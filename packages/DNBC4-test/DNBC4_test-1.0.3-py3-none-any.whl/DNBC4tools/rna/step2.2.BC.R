library(scHCL)
library(Seurat)
library(cowplot)
library(tidyr)
library(ggplot2)
library(RColorBrewer)
library(scMCA)
#library(SingleR)
#library(celldex)
library(patchwork)

#Get the parameters
parser = argparse::ArgumentParser(description="script to Batch correction and Cluster scRNA data")
parser$add_argument('-I','--input', help='input rds list')
parser$add_argument('-D','--dim',help='dim usage')
parser$add_argument('-PC','--pc',help='pc usage')
parser$add_argument('-O','--out',help='out directory')
parser$add_argument('-R','--removebatch',help='if remove sample batch')
parser$add_argument('-RES','--res',help='resolution usage')
parser$add_argument('-K','--knn',help='defines k for the k-nearest neighbor algorithm')
parser$add_argument('-MD','--maxdim',help='max dimension to keep from UMAP procedure')
parser$add_argument('-S','--seed',help='seed usage')
parser$add_argument('-SP','--species',help='sample from which species,human or mouse')
args = parser$parse_args()

remove_batch <- if(!is.null(args$removebatch)) args$removebatch else "TRUE"
dim.usage <- if(!is.null(args$dim)) args$dim else 30
pc.usage <- if(!is.null(args$pc)) args$pc else 50
seed.usage <- if(!is.null(args$seed)) args$seed else 0
k.usage <- if(!is.null(args$knn)) args$knn else 20
res.usage <- if(!is.null(args$res)) args$res else 0.8
maxdim.usage <- if(!is.null(args$maxdim)) args$maxdim else "2L"
species.usage <- if(!is.null(args$species)) args$species else "mouse"

### input RDS files
files <- as.vector(as.matrix(read.table(args$input,header=F,stringsAsFactors=F)))

### read data
objectlist <- list()
for(i in 1:length(files)){
  objectlist[[i]] <- readRDS(files[i])
}

if (length(files)>1){
  cat("The number of RDS inputed:",length(files),"\n")
  ### when RDS file >1 and remove_batch=T
  if(remove_batch == "TRUE" | remove_batch == "T"){
    ### Seurat Integrate
    objectlist <- lapply(X = objectlist, FUN = function(x) {
      x <- NormalizeData(x)
      x <- FindVariableFeatures(x, selection.method = "vst", nfeatures = 2000)
    })

    object.anchors <- FindIntegrationAnchors(object.list = objectlist, dims = 1:dim.usage)
    object.combined <- IntegrateData(anchorset = object.anchors, dims = 1:dim.usage)

    DefaultAssay(object.combined) <- "integrated"
    object.combined <- ScaleData(object.combined, verbose = FALSE)
    object.combined <- RunPCA(object.combined, npcs = pc.usage, seed.use = seed.usage,verbose = FALSE)
    object.combined <- RunUMAP(object.combined, reduction = "pca", dims = 1:dim.usage, seed.use = seed.usage, max.dim = maxdim.usage)
    object.combined <- FindNeighbors(object.combined, reduction = "pca", dims = 1:dim.usage, k.param = k.usage, annoy.metric = "euclidean")
    object.combined <- FindClusters(object.combined, resolution = as.numeric(res.usage), algorithm = 1, random.seed = seed.usage)
    # Visualization
    pdf(paste(args$out,"/Clustering/","clustering_plot.pdf",sep=""),12,5)
    p1 <- DimPlot(object.combined, reduction = "umap", group.by = "split")
    p2 <- DimPlot(object.combined, reduction = "umap", label = TRUE)
    print(plot_grid(p1, p2))
    dev.off()
    DefaultAssay(object.combined) <- "RNA"
  }else{
    ### remove_batch=F
    ### merge data
    object.combined <- merge(x = objectlist[[1]], y = objectlist[[-1]])
    object.combined <- ScaleData(object.combined, verbose = FALSE)
    object.combined <- RunPCA(object.combined, npcs = pc.usage, seed.use = seed.usage,verbose = FALSE)
    object.combined <- RunUMAP(object.combined, reduction = "pca", dims = 1:dim.usage, seed.use = seed.usage, max.dim = maxdim.usage)
    object.combined <- FindNeighbors(object.combined, reduction = "pca", dims = 1:dim.usage, k.param = k.usage, annoy.metric = "euclidean")
    object.combined <- FindClusters(object.combined, resolution = as.numeric(res.usage), algorithm = 1, random.seed = seed.usage)
    # Visualization
    pdf(paste(args$out,"/Clustering/","clustering_plot.pdf",sep=""),12,5)
    p1 <- DimPlot(object.combined, reduction = "umap", group.by = "split")
    p2 <- DimPlot(object.combined, reduction = "umap", label = TRUE)
    print(plot_grid(p1, p2))
    dev.off()
  }
}else{
  ### when RDS file = 1 (do not remove batch)
  cat("The number of RDS inputed:",length(files),"\n")
  object.combined <- objectlist[[1]]
  object.combined <- ScaleData(object.combined, verbose = FALSE)
  object.combined <- RunPCA(object.combined, npcs = as.numeric(pc.usage), seed.use = as.numeric(seed.usage),verbose = FALSE)
  object.combined <- RunUMAP(object.combined, reduction = "pca", dims = 1:dim.usage, seed.use = as.numeric(seed.usage), max.dim = as.character(maxdim.usage))
  object.combined <- FindNeighbors(object.combined, reduction = "pca", dims = 1:dim.usage, k.param = as.numeric(k.usage), annoy.metric = "euclidean")
  object.combined <- FindClusters(object.combined, resolution = as.numeric(res.usage), algorithm = 1, random.seed = as.numeric(seed.usage))
  # Visualization
  pdf(paste(args$out,"/Clustering/","clustering_plot.pdf",sep=""),12,5)
  p1 <- DimPlot(object.combined, reduction = "umap", group.by = "split")
  p2 <- DimPlot(object.combined, reduction = "umap", label = TRUE)
  print(plot_grid(p1, p2))
  dev.off()
}

cluster_ID=as.data.frame(Idents(object = object.combined))
cluster_cor= as.data.frame(Embeddings(object = object.combined,reduction = "umap"))
coor=cbind(cluster_ID,cluster_cor,object.combined[['nCount_RNA']],object.combined[['nFeature_RNA']])
colnames(coor) = c("Cluster","UMAP_1","UMAP_2","nUMI","nGene")
coorOrder = coor[order(coor$Cluster),]

temp <- coorOrder
names <- rownames(temp)
rownames(temp) <- NULL
dataTemp <- cbind(names,temp)

cluster_stat <- as.data.frame(table(coorOrder$Cluster))
cluster_stat_changeName <- data.frame(Cluster=cluster_stat$Var1,cellNum=cluster_stat$Freq)
cluster_cell <- dplyr::left_join(dataTemp,cluster_stat_changeName,by="Cluster")
cluster_cell_merge <- unite(cluster_cell, "Cluster", Cluster, cellNum, sep = " CellsNum: ")


rownames(cluster_cell_merge) <- cluster_cell_merge[,1]
cluster_cell_merge <- cluster_cell_merge[,-1]
write.csv(cluster_cell_merge, file=paste(args$out,"/Clustering/cluster.csv",sep=""),quote=FALSE)

#write.csv(coorOrder, file=paste(args$out,"/Clustering/cluster.csv",sep=""),quote=FALSE)
write.csv(cluster_stat, file=paste(args$out,"/Clustering/cluster_cell.stat",sep=""),quote=FALSE)
seurat_markers <- FindAllMarkers(object.combined)
write.csv(as.data.frame(seurat_markers[,c(6,5,1,2,3,4)]),file= paste0(args$out,"/Clustering/marker.csv"),quote=FALSE)

cat(paste("Number of cells used for clustering,", length(colnames(object.combined)), "\n",sep=""),file=paste(args$out,"/Clustering/cell_report_2.csv",sep=""))



## cell type annotation
#object.combined <- readRDS("clustering_object.RDS")

object.combined_for_annotation <- GetAssayData(object.combined, slot="data")
if (species.usage %in% c("mouse","Mouse","mm10","human","Human","hg19","hg38","Human_nucleus","hg19_premRNA","Mouse_nucleus")){
  if (species.usage == "mouse"||species.usage == "Mouse"||species.usage == "mm10"||species.usage == "Mouse_nucleus"){
      object.combined_cell_type <- scMCA(scdata = object.combined_for_annotation, numbers_plot = 3)
      out=as.data.frame(unlist(object.combined_cell_type$scMCA))
      }
  else if (species.usage == "human"||species.usage == "Human"||species.usage == "hg19"||species.usage == "hg38" ||species.usage == "Human_nucleus" || species.usage == "hg19_premRNA"){

I     # hpca.se <- HumanPrimaryCellAtlasData()
#      hpca.se <- get(load("/hwfssz5/ST_PRECISION/OCG/wuliang2_SingleCell/RNA_pipeline/scRNA_V2.3/PISA-master/Celltype/HumanPrimaryCellAtlasData.Rdata"))
#      object.combined.hesc <- SingleR(test = object.combined_for_annotation, ref = hpca.se,  
#                                    labels =  hpca.se$label.main,
#                                    assay.type.test = "logcounts",
#                                    assay.type.ref = "logcounts",)
#      out=as.data.frame(unlist(object.combined.hesc$labels))
#      rownames(out) <- rownames(object.combined.hesc)
      object.combined_cell_type <- scHCL(scdata = object.combined_for_annotation, numbers_plot = 3)
      out=as.data.frame(unlist(object.combined_cell_type$scHCL))
      }
  object.combined@meta.data$cell_type=out[match(rownames(object.combined@meta.data),rownames(out)),1]
  out_meta=object.combined@meta.data
  cluster_anno <- as.data.frame(table(object.combined@meta.data$cell_type,object.combined@meta.data$seurat_clusters))
  
  # cluster_anno[order(cluster_anno$Var2,-cluster_anno$Freq),]
  sorted_cluster_anno <- cluster_anno[order(cluster_anno$Var2,-cluster_anno$Freq),]
  finl_cluster_anno <- sorted_cluster_anno[!duplicated(sorted_cluster_anno$Var2),]
  #finl_cluster_anno <- finl_cluster_anno[,c(1,2)]
  colnames(finl_cluster_anno) <- c("predicated.cell.type","seurat_clusters","Freq")
  out_meta=object.combined@meta.data
  use=out_meta[,c(8,9)]
  use$ID=rownames(out_meta)
  res=merge(use,finl_cluster_anno,by="seurat_clusters")
  object.combined@meta.data$predicated.cell.type <- res[match(rownames(out_meta),res$ID),4]
  
  getPalette = colorRampPalette(brewer.pal(9, "Paired"))
  a=getPalette(length(unique(object.combined@meta.data$predicated.cell.type)))

  
  c3=DimPlot(object = object.combined, label = FALSE, group.by = "predicated.cell.type") +
    scale_color_manual(values = a) + NoLegend()
  
  table_cell.type=as.data.frame(table(as.character(object.combined@meta.data$predicated.cell.type)))
  colnames(table_cell.type)=c("predicated.cell.type","number")
  table_cell.type$ratio=table_cell.type$number/colSums(table_cell.type[2])
  table_cell.type$percentage=paste0(round(table_cell.type$ratio,digits = 4)*100,"%")
  table_cell.type$Samples=unique(object.combined@meta.data$split)
  order_table_cell.type=table_cell.type[order(table_cell.type$number,decreasing = T),]  
  c4 <- ggplot(order_table_cell.type,aes(x=Samples,y=ratio,fill=predicated.cell.type)) + geom_col(width = 0.6) +geom_text(aes(label = percentage),position=position_stack(vjust =0.5),size = 2) + theme_cowplot() + scale_fill_manual(values = a)  + scale_y_continuous(expand=c(0,0)) 

  layout <- "AAB"
 # png(paste(args$out,"/Clustering/cluster_annotation.png",sep=""),width = 990,height = 479)
  #print(c3)
  p3 <- c3 + c4 + plot_layout(design = layout)
#  ggsave(p3,filename = paste(args$out,"/Clustering/cluster_annotation.png",sep=""),width = 18,height = 9)
   ggsave(p3,filename = paste(args$out,"/Clustering/cluster_annotation.png",sep=""),width = 18,height = 9)
#dev.off()

#  pdf(paste(args$out,"/Clustering/cluster_annotation.pdf",sep=""),width = 18,height = 9)
 # print(c3)
 # c3 + c4 + plot_layout(design = layout)
  #dev.off()
 
  #svg(paste(args$out,"/Clustering/cluster_annotation.svg",sep=""),width = 990,height = 479)
  #print(c3)
  #c3 + c4 + plot_layout(design = layout)
  #dev.off()
  
 # table_cell.type=as.data.frame(table(as.character(object.combined@meta.data$predicated.cell.type)))
 # colnames(table_cell.type)=c("predicated.cell.type","number")
 # table_cell.type$ratio=table_cell.type$number/colSums(table_cell.type[2])
 # order_table_cell.type=table_cell.type[order(table_cell.type$number,decreasing = T),]
  order_table_cell.type <- order_table_cell.type[,c(1,2,3)]
  write.table(order_table_cell.type,file = paste(args$out,"/Clustering/celltypecount.csv",sep=""),sep = ",",quote = FALSE,row.names = FALSE)

}else{
print("There is no such species reference for annnotation")
ggsave(p2,filename = paste(args$out,"/Clustering/cluster_annotation.png",sep=""),width = 18,height = 9)
#library(scMCA)
#object.combined_cell_type <- scMCA(scdata = object.combined_for_annotation, numbers_plot = 3)
#out=as.data.frame(unlist(object.combined_cell_type$scMCA))
}

saveRDS(object.combined,paste0(args$out,"/Clustering/clustering_annotation_object.RDS"))

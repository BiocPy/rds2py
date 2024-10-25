# # pairlist

# y <- pairlist(runif(10), runif(20), runif(30))
# saveRDS(y, file="pairlist.rds")

# y <- pairlist(sample(letters), pairlist(sample(11), runif(12)))
# saveRDS(y, file="pairlist_nested.rds")

# y <- pairlist(foo=sample(letters), bar=pairlist(whee=sample(11), bum=runif(12))) # with names
# saveRDS(y, file="pairlist_names.rds")

# y <- pairlist(aaron=sample(letters), bar=list(sample(11), runif(12)))
# attr(y, "foo") <- "bar"
# saveRDS(y, file="pairlist_attr.rds")


# altrep

# scenarios <- 1:15
# saveRDS(y, file="altrep_series.rds")

# x <- 1:100
# names(x) <- sprintf("GENE_%s", seq_along(x))
# saveRDS(x, file="altrep_attr.rds")

# x <- as.character(1:100)
# saveRDS(x, file="altrep_strings_deferred.rds")

# x <- c(NA_integer_, 1:10, NA_integer_)
# x <- as.character(x)
# saveRDS(x, file="altrep_strings_wNA.rds")

# x <- as.character(1:100 * 2)
# saveRDS(x, file="altrep_double_deferred.rds")

# x <- c(NaN, 1:10, Inf, -Inf, NA)
# x <- as.character(x)
# saveRDS(x, file="altrep_double_wNA.rds")

# atomic

y <- rpois(112, lambda=8)
saveRDS(y, file="atomic_ints.rds")

y <- rbinom(55, 1, 0.5) == 0
saveRDS(y, file="atomic_logical.rds")

y <- rbinom(999, 1, 0.5) == 0
y[sample(length(y), 10)] <- NA
saveRDS(y, file="atomic_logical_wNA.rds")

y <- rnorm(99)
saveRDS(y, file="atomic_double.rds")

y <- as.raw(sample(256, 99, replace=TRUE) - 1)
saveRDS(y, file="atomic_raw.rds")

y <- rnorm(99) + rnorm(99) * 1i
saveRDS(y, file="atomic_complex.rds")

y <- sample(LETTERS)
saveRDS(y, file="atomic_chars.rds")

y <- c("α-globin", "😀😀😀", "fußball", "Hervé Pagès")
saveRDS(y, file="atomic_chars_unicode.rds")

vals <- sample(.Machine$integer.max, 1000)
names(vals) <- sprintf("GENE_%i", seq_along(vals))
attr(vals, "foo") <- c("BAR", "bar", "Bar")
class(vals) <- "frog"
saveRDS(vals, file="atomic_attr.rds")

# scalars

y <- 10
saveRDS(y, file="scalar_int.rds")

# lists

y <- list(runif(10), runif(20), runif(30))
saveRDS(y, file="lists.rds")

y <- list(sample(letters), list(sample(11), runif(12)))
saveRDS(y, file="lists_nested.rds")

y <- list(list(2, 6), list(5, c("cat", "dog", "bouse"), list(sample(99), runif(20))))
saveRDS(y, file="lists_nested_deep.rds")

df <- data.frame(xxx=runif(19), YYY=sample(letters, 19), ZZZ=rbinom(19, 1, 0.4) == 0)
saveRDS(df, file="lists_df.rds")

rownames(df) <- paste0("FOO-", LETTERS[1:19])
saveRDS(df, file="lists_df_rownames.rds")

# S4

y <- Matrix::rsparsematrix(100, 10, 0.05)
saveRDS(y, file="s4_matrix.rds")

setClass("FOO", slots=c(bar="integer"))
y <- new("FOO", bar=2L)
saveRDS(y, file="s4_class.rds")

# GenomicRanges

gr <- GRanges(
    seqnames = Rle(c("chr1", "chr2", "chr1", "chr3"), c(1, 3, 2, 4)),
    ranges = IRanges(101:110, end = 111:120, names = head(letters, 10)),
    strand = Rle(strand(c("-", "+", "*", "+", "-")), c(1, 2, 2, 3, 2)),
    score = 1:10,
    GC = seq(1, 0, length=10))

saveRDS(gr, file="granges.rds")

# factors

f1 <- factor(c("chr1", "chr2", "chr1", "chr3"))
saveRDS(f1, "simple_factors.rds")

# Rle
x2 <- Rle(LETTERS[c(21:26, 25:26)], 8:1)
saveRDS(x2, "simple_rle.rds")


# SummarizedExperiment

nrows <- 200
ncols <- 6
counts <- matrix(runif(nrows * ncols, 1, 1e4), nrows)
rowRanges <- GRanges(rep(c("chr1", "chr2"), c(50, 150)),
                     IRanges(floor(runif(200, 1e5, 1e6)), width=100),
                     strand=sample(c("+", "-"), 200, TRUE),
                     feature_id=sprintf("ID%03d", 1:200))
rowd <- DataFrame(seqs = rep(c("chr1", "chr2"), c(50, 150)))
colData <- DataFrame(Treatment=rep(c("ChIP", "Input"), 3),
                     row.names=LETTERS[1:6])

se <- SummarizedExperiment(assays=list(counts=counts),
                     rowData = rowd, colData=colData)

rse <- SummarizedExperiment(assays=list(counts=counts),
                            rowRanges = rowRanges, colData=colData)
saveRDS(se, "sumexpt.rds")
saveRDS(rse, "ranged_se.rds")

# SingleCell Experiment

library(scRNAseq)
sce <- ReprocessedAllenData("tophat_counts")
sce_subset <- sce[1:100, 1:100]
saveRDS(sce_subset, "simple_sce.rds")

# lists

x <- list(github = "jkanche", fullname=c("Kancherla", "Jayaram"),
          collab=list(github = "ltla", fullname=c("Lun", "Aaron")))
saveRDS(x, "simple_list.rds")

# frames
dframe <- as.data.frame(lists_df)
saveRDS(dframe, "data.frame.rds")

# MAE
library(MultiAssayExperiment)
patient.data <- data.frame(sex=c("M", "F", "M", "F"),
                           age=38:41,
                           row.names=c("Jack", "Jill", "Bob", "Barbara"))

exprss1 <- matrix(rnorm(16), ncol = 4,
                  dimnames = list(sprintf("ENST00000%i", sample(288754:290000, 4)),
                                  c("Jack", "Jill", "Bob", "Bobby")))
exprss2 <- matrix(rnorm(12), ncol = 3,
                  dimnames = list(sprintf("ENST00000%i", sample(288754:290000, 4)),
                                  c("Jack", "Jane", "Bob")))
doubleExp <- list("methyl 2k"  = exprss1, "methyl 3k" = exprss2)
simpleMultiAssay <- MultiAssayExperiment(experiments=doubleExp)
simpleMultiAssay2 <- MultiAssayExperiment(experiments=doubleExp,
                                          colData=patient.data)
saveRDS(simpleMultiAssay2, "simple_mae.rds")

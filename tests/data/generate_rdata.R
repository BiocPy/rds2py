set.seed(42)

# Simple RData with basic types
int_vec <- as.integer(c(1, 2, 3, 4, 5))
dbl_vec <- c(1.1, 2.2, 3.3, 4.4, 5.5)
str_vec <- c("hello", "world", "foo")
bool_vec <- c(TRUE, FALSE, TRUE, TRUE, FALSE)
save(int_vec, dbl_vec, str_vec, bool_vec, file = "simple.RData")

# Single object RData
single_obj <- as.integer(1:10)
save(single_obj, file = "single_object.RData")

# RData with a data.frame
test_df <- data.frame(
    x = 1:5,
    y = c(1.1, 2.2, 3.3, 4.4, 5.5),
    z = c("a", "b", "c", "d", "e"),
    stringsAsFactors = FALSE
)
save(test_df, file = "dataframe.RData")

# RData with a list
test_list <- list(a = 1:3, b = c("x", "y"), c = TRUE)
save(test_list, file = "list.RData")

# RData with a matrix
test_matrix <- matrix(1:12, nrow = 3, ncol = 4)
save(test_matrix, file = "matrix.RData")

# RData with multiple mixed types
nums <- c(10.0, 20.0, 30.0)
chars <- LETTERS[1:5]
ints <- as.integer(c(100, 200, 300))
nested_list <- list(alpha = 1:3, beta = c("a", "b"))
save(nums, chars, ints, nested_list, file = "mixed.RData")

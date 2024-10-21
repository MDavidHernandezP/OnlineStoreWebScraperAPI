# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset <- data.frame(undefined, undefined.1, undefined.2)
# dataset <- unique(dataset)

# Paste or type your script code here:

boxplot(Price ~ Rating, # meta_score with respect of platform.
        data = dataset, # Specify data source.
        col = "purple",
        # To show only this 5 platforms.
        subset = Rating %in% c(4.6, 4.7, 4.8, 4.9, 5),
        xlab = "Top 5 Ratings",
        ylab = "Prices",
        fram = FALSE
        )
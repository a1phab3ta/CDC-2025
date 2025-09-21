# ExoRad

**A tape measure for your telescope!**

### Motivation
Around a third of exoplanets have no estimated radius. Without this information, we miss key insights about the composite material density and surface gravity's effects on the planet's climate and geology. Thus, ExoRad implements machine learning to find these unkown radii.

## Inspiration
We chose the natural science track, where we were tasked to investigate the features of planetary data. We noticed that out of all planet entries, roughly a third of them were missing its radius, despite often repeated reports on the same planets. The radius of a planet is one of its most important features, since it is important for inference on a planet’s density, material composition, surface gravity, and potential for life. Thus, we found it natural to consider what other (more documented) features of a planet can be used to predict a planet’s radius. 

## What it does
ExoRad takes fields in the dataset: semi-major axis, equilibrium temperature, insolation flux, eccentricity and orbital period. Then, it will estimate the radius of the planet in units of “Earths”, with a standard error of 25%.


## How we built it
After selecting the parameters we thought would be most impactful in predicting the radius, we did data cleaning, removing all the rows with null values for any of our fields. We then tried two different types of algorithms, gradient descent (Barzilai-Borwein method) and regression algorithms (Random Forest, XGBoost and SVM). The Random Forest Regressor performed the best out of all the regressors, so we moved forward with that. Following that, we tried many optimization methods like standardization, feature selection, filters and parameter tuning, resulting in a 25.0% error for Random Forest Regression, while gradient descent had a 42.5% error. 

## Challenges we ran into
Our gradient descent model ran into problems in calculating the adaptive learning rate. Since components in its calculation often involved dividing by value on the order of 10^-16, floating point errors became non-negligible, leading to large learning rates when not intended. We adapted to this by flooring how small this division could be at 5*10^-15 to get more reasonable learning rates, leading to a sizable decrease in prediction error. 
We also had some issues collaborating on the same file in real time. Tools that we previously had experience with, like VSCode LiveShare and Google Colab, were not working and did not allow us to the same file without issues. GitHub also shared the same problem with frequent merging conflicts occurring. In the end, we had to either work on separate files or use one computer, which we eventually got used to and were able to successfully finish the project. 


## Accomplishments that we're proud of
We are proud of our best error rate of 25%, much lower than we initially expected to have due to high error margins in the data. Many of the data points have their own error bars with more than a 25% possible error, which would make it more difficult for our model. We are also proud of our focus and determination in trying as many optimization methods as possible to get the best result. We spent many hours at the drawing board thinking of any method that could possibly improve our model. In total, these optimizations improved each model by over 2.5x. 

## What we learned
Throughout this project, we learned how beneficial machine learning is for problems where no clear connections between data points and the desired value are possible. None of the data we gave these models directly corresponds to radius, but by having a bevy of related values, we still managed to get reasonable estimates of the planetary radii. This is a unique feature of machine learning, and one often overlooked among discussions of its usefulness in qualitative analysis. Furthermore, we learned the importance of various optimizations, like natural log standardization, which halved the output error for the second model. 

## What's next for ExoRad
Our two models were able to predict the radii of planets from a test training set within reasonable error, given that these radii are typically already reported with a large margin of error. We hope to be able to implement these models outside our training set to planets with unknown radii so we can gain more insight into the characteristics of discovered planets. 

*Submission for the 2025 Carolina Data Challenge by Brendan Apple, Sumehra Choudhury, Pranav Nair, Thomas Di Maggio*

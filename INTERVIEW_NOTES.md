# Interview Notes

This file is for you, not for recruiters. It gives you talking points and
practice questions so you can explain this project with confidence. Read it,
practise the answers out loud, and make sure every line is true for you. The
fastest way to lose credibility is to claim something you cannot explain, so if
any part below is unclear, that is your signal to go and learn it first.

## Your 60 second project summary

Practise something like this until it feels natural:

> "I built an end to end project answering the question 'what makes a car fuel
> efficient?' using real EPA fuel economy data for 234 cars. I cleaned and
> prepared the data in Python, including splitting the transmission field into
> type and gear count. I loaded it into a SQLite database and used SQL to break
> economy down by engine size, cylinders, class and so on. Then I built a simple
> linear regression in numpy that predicts a car's economy from its engine size
> and cylinder count. It explains about two thirds of the variation with a
> typical error of around 2 mpg. The clearest finding was that cylinder count
> and engine size are by far the biggest drivers of fuel economy."

## Questions you should be ready for

**Why is the dataset so small, only 234 cars?**
It is a real, well known dataset published by the EPA, and I chose it because I
could work with the whole thing properly rather than a sample. The techniques
are identical on a larger dataset. If pushed, I would say the next version would
use a bigger, more recent dataset including hybrids and electric cars.

**What cleaning and preparation did you do?**
I checked for missing values and duplicates first. The data was complete. The
main work was preparation: I turned short codes into readable words (drivetrain
and fuel type), split the "trans" field, for example "auto(l5)", into a
transmission type and a gear count, handled a few gearboxes that had no fixed
gear count, and added a single combined economy figure as the average of city
and highway.

**You found 9 identical rows. Why not remove them?**
Because in this dataset they are not errors. They are separate real car models
that happen to share every listed specification. Removing them would delete real
records. The point is that I made that call deliberately rather than blindly
running a remove duplicates command.

**Explain your most advanced SQL query.**
Query 10 finds the most efficient car in each class using a window function.
RANK() OVER (PARTITION BY class ORDER BY avg_mpg DESC) numbers the cars inside
each class from most efficient downwards, without merging rows the way GROUP BY
would. The outer query then keeps only rank 1 per class. One class shows two
number ones because there was a tie, which is exactly how RANK is supposed to
behave.

**Explain your model. What is R squared?**
It is a linear regression: it finds the straight-line relationship between a
car's engine size and cylinder count and its fuel economy, by choosing the line
that makes the total squared error smallest. R squared is the share of the
variation in economy that the model explains, from 0 to 1. Mine is about 0.64,
so it explains roughly two thirds. The typical prediction is off by about 2 mpg.

**What are the model's weaknesses?**
Two main ones. First, engine size and cylinder count move together, so the model
cannot fully separate their individual effects. Second, it is a straight-line
fit, so it is least accurate for the most efficient cars, where the real
relationship curves. You can see this on the predicted-versus-actual chart,
where the very efficient cars are under-predicted.

**Could you have done the analysis in SQL or Python only?**
Yes, and I did some of it both ways on purpose. SQL is strong for grouping and
summarising data in a database. Python with pandas is strong for flexible
analysis, charting and modelling. Real analysts move between the two.

**Why build the model with numpy instead of scikit-learn?**
So nothing is hidden. I wanted to be able to explain exactly what least squares
does rather than call a function I could not describe. On a bigger project I
would use scikit-learn for convenience, but the maths would be the same.

## Honesty checklist

Before you put this on your CV, make sure you can honestly say yes to all of
these:

- I can explain what every script does in plain English.
- I can read any SQL query here and say what it returns.
- I understand each cleaning and preparation step and why I did it.
- I can explain, simply, what the model does and what R squared means.
- I know the main findings and can point to the chart that shows each one.
- I have run the whole thing myself from start to finish.

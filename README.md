# ml_nba3: NBA Game Outcome Prediction

This project was a hands-on experience to learn Python and Machine Learning so many, many errors were committed.

The goal was to predict the outcomes of NBA games using machine learning techniques. NBA game data was scraped, processed, and used to build predictive models to forecast whether a team will win or lose a game.

## Project Overview

- **Data Collection**:
  - Scraped data from official NBA statistics websites, including box scores, player performance, and team statistics.
  - The dataset covers games from multiple seasons.

- **Feature Engineering**:
  - Relevant features such as team performance metrics, player averages, and recent form were used.
  - Feature scaling and normalization are applied to ensure consistent model performance.

- **Machine Learning Models**:
  - Various models, including logistic regression, decision trees, and neural networks.
  - Model hyperparameters are tuned to optimize accuracy.

- **Evaluation and Deployment**:
  - Evaluated model performance using metrics like accuracy and value of a potential bet (on either the loser or winner of the match) given the confidence of a prediction.

## Packages Used
- **selenium**: For web scraping pages with javascript elements.
- **numpy** and **pandas**: Data manipulation libraries for structured data.
- **scikit-learn**: Machine learning algorithms.
- **matplotlib**: Plotting library for visualizations.
- **pytorch**: For the neural network models.

## Results
Most models were ~3-6% worse than a betting company at predicting the winner of a NBA match.

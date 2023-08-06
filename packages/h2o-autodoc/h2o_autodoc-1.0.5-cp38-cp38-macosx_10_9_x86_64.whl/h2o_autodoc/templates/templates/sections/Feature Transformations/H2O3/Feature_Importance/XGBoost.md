XGBoost\'s feature importance is calculated from the gains of its loss
functions during tree construction.

Where gain is defined as:

$$Gain = \frac{1}{2}\lbrack\frac{G_{L}^{2}}{H_{L} + \lambda} + \frac{G_{R}^{2}}{H_{R} + \lambda} - \frac{(G_{L} + G_{R})^{2}}{H_{L} + H_{R} + \lambda}\rbrack - \gamma$$

**XGBoost Feature Importance Reference**

Chen, Tianqi, and Carlos Guestrin. \"Xgboost: A scalable tree boosting
system.\" Proceedings of the 22nd acm sigkdd international conference on
knowledge discovery and data mining. 2016.

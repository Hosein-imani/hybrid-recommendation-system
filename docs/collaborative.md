# Collaborative Filtering

[🇺🇸 English](#english) | [🇮🇷 فارسی](#persian)

<a id="english"></a>

## 🇺🇸 English

### Overview

The Collaborative module learns from user–movie ratings instead of relying on movie metadata. It uses the Surprise <code>SVD</code> algorithm to learn latent relationships between users and movies.

~~~mermaid
flowchart LR
    A[Ratings data] --> B[Surprise dataset]
    B --> C[Train / test split]
    C --> D[SVD matrix factorization]
    D --> E[RMSE and MAE evaluation]
    D --> F[Predicted ratings]
    F --> G[Top-N unseen movies]
~~~

### Model Workflow

The Collaborative pipeline:

1. loads the ratings and movie metadata;
2. converts the ratings into the format required by Surprise;
3. creates a reproducible train/test split;
4. trains an SVD model with configurable hyperparameters;
5. evaluates rating prediction using RMSE and MAE;
6. predicts ratings for movies the user has not rated;
7. returns the highest-ranked candidates with their movie metadata.

SVD is a matrix factorization method. Instead of comparing genres directly, it learns hidden user and movie representations from historical rating behavior.

### Main Components

- <code>src/collaborative/model.py</code> prepares the Surprise dataset, trains SVD, predicts ratings, and saves or loads model artifacts.
- <code>src/collaborative/evaluator.py</code> calculates RMSE, MAE, and the number of evaluated predictions.
- <code>src/collaborative/recommender.py</code> generates Top-N recommendations and removes movies already present in the user's training history.

Joblib is used to persist the trained model and trainset, allowing them to be loaded later without repeating the training step.

### Project Structure

The following tree shows the files currently used by the Collaborative module:

~~~text
src/
└── collaborative/
    ├── model.py
    ├── evaluator.py
    └── recommender.py

scripts/
└── collaborative/
    ├── run_svd.py
    └── test_collaborative.py
~~~

### Outputs

Training generates the following artifacts:

~~~text
outputs/
└── collaborative/
    ├── reports/
    │   └── svd_evaluation_report.txt
    │
    ├── recommendations/
    │   └── user_1_recommendations.csv
    │
    └── models/
        ├── svd_model.pkl
        ├── trainset.pkl
        └── metadata.json
~~~

### Running the Pipeline

Train, evaluate, save the model, and generate a sample recommendation list:

~~~bash
python scripts/collaborative/run_svd.py
~~~

To load the saved model and request recommendations for another user:

~~~bash
python scripts/collaborative/test_collaborative.py
~~~

The generated reports, recommendation tables, model artifacts, and showcase visuals are organized by module under <code>outputs/collaborative/</code> and <code>outputs/showcase/</code>.

### Evaluation

The current model evaluation uses:

- RMSE, which penalizes larger prediction errors more strongly;
- MAE, which measures the average absolute prediction error.

These metrics evaluate rating prediction quality. Ranking metrics can be added later when the project moves toward a production-oriented evaluation setup.

<a id="persian"></a>

## 🇮🇷 راهنمای فارسی

### معرفی

ماژول Collaborative به‌جای تکیه بر اطلاعات محتوایی فیلم، از سابقه‌ی امتیازدهی کاربران یاد می‌گیرد. این ماژول از الگوریتم <code>SVD</code> در کتابخانه‌ی Surprise استفاده می‌کند تا رابطه‌های نهفته بین کاربران و فیلم‌ها را پیدا کند.

~~~mermaid
flowchart LR
    A[داده‌ی امتیازها] --> B[ Surprise دیتاست]
    B --> C[تقسیم آموزش و آزمون]
    C --> D[SVD فاکتورگیری ماتریس با]
    D --> E[ RMSE و MAE ارزیابی با]
    D --> F[امتیازهای پیش‌بینی‌شده]
    F --> G[فیلم‌های ندیده Top-N پیشنهاد]
~~~

### روند کار مدل

پایپ لاین مربوط به Collaborative این مراحل را انجام می‌دهد:

1. داده‌ی امتیازها و اطلاعات فیلم‌ها را می‌خواند؛
2. داده‌ی امتیازها را به قالب مورد نیاز Surprise تبدیل می‌کند؛
3. داده را با یک تقسیم‌بندی ثابت و قابل تکرار به دو بخش آموزش و آزمون تقسیم می‌کند؛
4. مدل SVD را با hyperparameterهای قابل تنظیم آموزش می‌دهد؛
5. دقت پیش‌بینی امتیازها را با RMSE و MAE ارزیابی می‌کند؛
6. برای فیلم‌هایی که کاربر قبلاً امتیاز نداده است، امتیاز تخمینی محاسبه می‌کند؛
7. بهترین گزینه‌ها را همراه با اطلاعات فیلم برمی‌گرداند.

الگوی svd یک روش فاکتورگیری ماتریس است این الگوریتم به‌ جای مقایسه‌ی مستقیم ژانرها از سابقه‌ی امتیازدهی کاربران برای یادگیری نمایش‌های نهفته‌ی کاربران و فیلم‌ها استفاده می‌کند

### اجزای اصلی

* فایل `src/collaborative/model.py` دیتاست `Surprise` را آماده می‌کند، مدل `SVD` را آموزش می‌دهد، امتیازها را پیش‌بینی می‌کند و فایل‌های مدل را ذخیره یا بارگذاری می‌کند.
* فایل `src/collaborative/evaluator.py` مقدار `RMSE`، `MAE` و تعداد پیش‌بینی‌های ارزیابی‌شده را محاسبه می‌کند.
* فایل `src/collaborative/recommender.py` پیشنهادهای `Top-N` را می‌سازد و فیلم‌هایی را که در سابقه‌ی آموزشی کاربر وجود دارند، از نتیجه کنار می‌گذارد.


برای ذخیره‌ی مدل آموزش‌دیده و trainset از Joblib استفاده شده است؛ بنابراین در اجرای بعدی می‌توان آن‌ها را بارگذاری کرد و مدل را دوباره آموزش نداد.

### ساختار پروژه

درخت زیر فایل‌هایی را نشان می‌دهد که در حال حاضر برای ماژول پیشنهاددهی Collaborative استفاده می‌شوند:

~~~text
src/
└── collaborative/
    ├── model.py
    ├── evaluator.py
    └── recommender.py

scripts/
└── collaborative/
    ├── run_svd.py
    └── test_collaborative.py
~~~

### خروجی‌ها

پس از آموزش مدل، فایل‌های زیر تولید می‌شوند:

~~~text
outputs/
└── collaborative/
    ├── reports/
    │   └── svd_evaluation_report.txt
    │
    ├── recommendations/
    │   └── user_1_recommendations.csv
    │
    └── models/
        ├── svd_model.pkl
        ├── trainset.pkl
        └── metadata.json
~~~

### اجرای Pipeline

برای آموزش مدل، ارزیابی آن، ذخیره‌ی artifactها و تولید یک نمونه از پیشنهادها:

~~~bash
python scripts/collaborative/run_svd.py
~~~

برای بارگذاری مدل ذخیره‌شده و گرفتن پیشنهاد برای یک کاربر دیگر:

~~~bash
python scripts/collaborative/test_collaborative.py
~~~

گزارش‌ها، جدول‌های پیشنهاد، artifactهای مدل و نمونه‌های تصویری در پوشه‌های مربوط به Collaborative داخل <code>outputs/collaborative/</code> و <code>outputs/showcase/</code> قرار می‌گیرند.

### ارزیابی مدل

مدل فعلی با دو معیار ارزیابی می‌شود:

- RMSE که خطاهای بزرگ‌تر را با شدت بیشتری جریمه می‌کند؛
- MAE که میانگین قدرمطلق خطاهای پیش‌بینی را نشان می‌دهد.

این معیارها کیفیت پیش‌بینی امتیاز را بررسی می‌کنند. در مراحل بعد می‌توان معیارهای رتبه‌بندی را نیز برای ارزیابی دقیق‌تر کیفیت پیشنهادها اضافه کرد.


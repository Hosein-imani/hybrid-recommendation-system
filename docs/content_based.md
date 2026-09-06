# Content-Based Recommendation

[🇺🇸 English](#english) | [🇮🇷 فارسی](#persian)

<a id="english"></a>

## 🇺🇸 English

### Overview

The Content-Based module recommends movies with similar metadata. In the current implementation, the main content feature is the genre list of each movie.

~~~mermaid
flowchart LR
    A[Selected movie or movies] --> B[Movie preprocessing]
    B --> C[One-hot genre matrix]
    C --> D[Preference profile]
    D --> E[Cosine similarity]
    E --> F[Remove input movies and rank]
    F --> G[Top-N recommendations]
~~~

### How It Works

1. Movie titles are cleaned and genres are converted into lists.
2. <code>FeatureEngineer</code> creates a numerical genre matrix.
3. Each movie is represented by a vector whose columns describe its genres.
4. <code>SimilarityCalculator</code> builds a profile from one or more selected movies.
5. Cosine similarity is calculated between the profile and all movie vectors.
6. The selected movies are removed, and the highest-scoring candidates are returned.

When multiple movies are provided, their feature vectors are averaged into one profile. This allows the query to represent a broader preference instead of relying on a single title.

### Main Components

- <code>src/content_based/feature_engineering.py</code> creates the genre features.
- <code>src/content_based/similarity.py</code> validates movie IDs, calculates similarity, and ranks candidates.
- <code>src/content_based/recommender.py</code> provides the recommendation interface.

The similarity layer also checks that requested movie IDs exist and rejects duplicate input IDs.

### Project Structure

The following tree shows the files currently used by the Content-Based module:

~~~text
src/
└── content_based/
    ├── feature_engineering.py
    ├── similarity.py
    └── recommender.py

scripts/
└── content_based/
    ├── run_feature_engineering.py
    ├── run_similarity.py
    ├── run_recommender.py
    └── test_content_based.py
~~~

### Outputs

The Content-Based pipeline organizes its artifacts as follows:

~~~text
outputs/
└── content_based/
    ├── feature_engineering/
    │   ├── artifacts/
    │   │   └── genre_matrix.csv
    │   ├── reports/
    │   │   └── feature_engineering_report.txt
    │   └── visualizations/
    ├── similarity/
    │   ├── artifacts/
    │   │   └── top_similar_movies.csv
    │   ├── reports/
    │   │   └── similarity_report.txt
    │   └── visualizations/
    └── recommender/
        ├── recommendations/
        │   └── recommendations.csv
        ├── reports/
        │   └── recommendation_report.txt
        └── visualizations/
~~~

### Running the Pipeline

Run these commands from the repository root:

~~~bash
python scripts/content_based/run_feature_engineering.py
python scripts/content_based/run_similarity.py
python scripts/content_based/run_recommender.py
~~~

To test the recommender with selected movie titles:

~~~bash
python scripts/content_based/test_content_based.py
~~~

The scripts write reports, feature artifacts, recommendation tables, and visual outputs under <code>outputs/content_based/</code>.

### Why This Approach?

Content-Based filtering is explainable and does not require a large user interaction history. A recommendation can be understood by comparing the genres of the selected movies with the genres of the returned candidates.

The module is intentionally independent from the Collaborative model, which makes it easy to extend later with richer metadata such as descriptions, keywords, cast, or directors.

<a id="persian"></a>

## 🇮🇷 راهنمای فارسی

### معرفی

ماژول Content-Based فیلم‌هایی را پیشنهاد می‌دهد که از نظر اطلاعات محتوایی به فیلم‌های انتخاب‌شده شباهت دارند. در نسخه‌ی فعلی، ویژگی اصلی هر فیلم فهرست ژانرهای آن است.

~~~mermaid
flowchart LR
    A[یک یا چند فیلم انتخابی] --> B[پیش‌پردازش فیلم‌ها]
    B --> C[ماتریس one-hot ژانرها]
    C --> D[پروفایل سلیقه]
    D --> E[Cosine similarity]
    E --> F[حذف فیلم‌های ورودی و مرتب‌سازی]
    F --> G[پیشنهادهای Top-N]
~~~

### روند کار

1. عنوان فیلم‌ها تمیز می‌شود و ژانرها به فهرست تبدیل می‌شوند.
2. کلاس <code>FeatureEngineer</code> ماتریس عددی ژانرها را می‌سازد.
3. هر فیلم به‌صورت یک بردار نمایش داده می‌شود و ستون‌های این بردار، ژانرهای فیلم را نشان می‌دهند.
4. <code>SimilarityCalculator</code> با استفاده از یک یا چند فیلم انتخابی، یک پروفایل سلیقه می‌سازد.
5. شباهت cosine بین این پروفایل و بردار همه‌ی فیلم‌ها محاسبه می‌شود.
6. فیلم‌های ورودی از نتیجه حذف می‌شوند و نزدیک‌ترین گزینه‌ها بر اساس امتیاز شباهت برگردانده می‌شوند.

اگر چند فیلم انتخاب شود، بردارهای ویژگی آن‌ها میانگین‌گیری می‌شوند و یک پروفایل مشترک می‌سازند. بنابراین نتیجه فقط به یک عنوان وابسته نمی‌ماند و می‌تواند سلیقه‌ی گسترده‌تری را نشان دهد.

### اجزای اصلی

- <code>src/content_based/feature_engineering.py</code> ویژگی‌های ژانری را ایجاد می‌کند.
- <code>src/content_based/similarity.py</code> شناسه‌ی فیلم‌ها را بررسی می‌کند، شباهت را محاسبه می‌کند و نتیجه را مرتب می‌کند.
- <code>src/content_based/recommender.py</code> رابط اصلی پیشنهاددهی را فراهم می‌کند.

لایه‌ی محاسبه‌ی شباهت بررسی می‌کند که شناسه‌های واردشده در داده وجود داشته باشند و شناسه‌ی تکراری در ورودی پذیرفته نشود.

### ساختار پروژه

درخت زیر فایل‌هایی را نشان می‌دهد که در حال حاضر برای ماژول پیشنهاددهی مبتنی بر محتوا استفاده می‌شوند:

~~~text
src/
└── content_based/
    ├── feature_engineering.py
    ├── similarity.py
    └── recommender.py

scripts/
└── content_based/
    ├── run_feature_engineering.py
    ├── run_similarity.py
    ├── run_recommender.py
    └── test_content_based.py
~~~

### خروجی‌ها

Pipeline مربوط به Content-Based، خروجی‌های خود را در ساختار زیر دسته‌بندی می‌کند:

~~~text
outputs/
└── content_based/
    ├── feature_engineering/
    │   ├── artifacts/
    │   │   └── genre_matrix.csv
    │   ├── reports/
    │   │   └── feature_engineering_report.txt
    │   └── visualizations/
    ├── similarity/
    │   ├── artifacts/
    │   │   └── top_similar_movies.csv
    │   ├── reports/
    │   │   └── similarity_report.txt
    │   └── visualizations/
    └── recommender/
        ├── recommendations/
        │   └── recommendations.csv
        ├── reports/
        │   └── recommendation_report.txt
        └── visualizations/
~~~

### اجرای Pipeline

این دستورها را از ریشه‌ی مخزن اجرا کنید:

~~~bash
python scripts/content_based/run_feature_engineering.py
python scripts/content_based/run_similarity.py
python scripts/content_based/run_recommender.py
~~~

برای آزمایش پیشنهاددهنده با چند عنوان فیلم انتخابی:

~~~bash
python scripts/content_based/test_content_based.py
~~~

این اسکریپت‌ها گزارش‌ها، artifactهای ویژگی، جدول‌های پیشنهاد و خروجی‌های تصویری را داخل <code>outputs/content_based/</code> قرار می‌دهند.

### چرا این روش؟

فیلتر مبتنی بر محتوا قابل توضیح است و برای کاربر جدید به سابقه‌ی طولانی از تعامل‌ها نیاز ندارد. می‌توان دلیل هر پیشنهاد را با مقایسه‌ی ژانرهای فیلم‌های انتخابی و فیلم‌های پیشنهادی توضیح داد.

این ماژول از مدل Collaborative مستقل است؛ بنابراین در آینده می‌توان ویژگی‌های بیشتری مانند خلاصه‌ی داستان، keywordها، بازیگران یا کارگردان را به آن اضافه کرد.


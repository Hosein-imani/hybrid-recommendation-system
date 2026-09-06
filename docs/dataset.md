# Dataset Pipeline

[🇺🇸 English](#english) | [🇮🇷 فارسی](#persian)

<a id="english"></a>

## 🇺🇸 English

### Overview

The dataset module is the shared foundation for the Content-Based, Collaborative, and Hybrid recommendation approaches. It loads the raw files, checks their quality, and prepares them for the recommendation modules.

Keeping these responsibilities separate makes the project easier to maintain and allows the data source or preprocessing steps to evolve independently from the recommendation logic.

~~~mermaid
flowchart LR
    A[Raw CSV files] --> B[DataLoader]
    B --> C[DataValidator]
    B --> D[DataPreprocessor]
    C --> E[Quality reports]
    D --> F[Prepared datasets]
    F --> G[Recommendation modules]
~~~

### Input Data

The project expects two files under <code>data/raw/</code>:

| File | Main columns | Purpose |
| --- | --- | --- |
| <code>movies.csv</code> | <code>movieId</code>, <code>title</code>, <code>genres</code> | Movie metadata |
| <code>ratings.csv</code> | <code>userId</code>, <code>movieId</code>, <code>rating</code>, <code>timestamp</code> | User–movie interactions |

The raw dataset is tracked with Git LFS because of its size.

### Main Components

- <code>src/data/loader.py</code> loads the raw CSV files and reports a clear error when a required file is missing.
- <code>src/data/validator.py</code> reports dataset dimensions, data types, missing values, and duplicate rows.
- <code>src/data/preprocessor.py</code> prepares movie and rating data for the recommendation modules.

### Project Structure

The following tree shows the files currently used by the dataset module:

~~~text
src/
└── data/
    ├── loader.py
    ├── validator.py
    └── preprocessor.py

scripts/
└── dataset/
    ├── analyze_dataset.py
    ├── preprocess_dataset.py
    └── validate_dataset.py
~~~

### Outputs

The dataset scripts generate reports in the following structure:

~~~text
outputs/
└── dataset_analysis/
    └── reports/
        ├── dataset_summary.txt
        ├── preprocessing_report.txt
        └── validation_report.txt
~~~

### Preprocessing

For the movies dataset, the pipeline:

1. extracts the release year from the movie title;
2. removes the year from the display title;
3. converts the pipe-separated genre string into a list.

For the ratings dataset, <code>timestamp</code> is removed before modeling because the current recommendation models do not use temporal information yet.

### Running the Dataset Scripts

Run these commands from the repository root:

~~~bash
python scripts/dataset/analyze_dataset.py
python scripts/dataset/validate_dataset.py
python scripts/dataset/preprocess_dataset.py
~~~

The generated reports provide a quick view of the input data, validation results, and preprocessing changes.

### Design Principle

The data layer follows a clear separation of responsibilities:

- loading retrieves the data;
- validation checks data quality;
- preprocessing transforms the data.

This separation keeps data preparation independent from the recommendation algorithms.

<a id="persian"></a>

## 🇮🇷 راهنمای فارسی

### معرفی Pipeline داده

ماژول داده، پایه‌ی مشترک هر سه روش پیشنهاددهی Content-Based، Collaborative و Hybrid است. این ماژول فایل‌های خام را می‌خواند، کیفیت آن‌ها را بررسی می‌کند و داده را برای استفاده‌ی ماژول‌های پیشنهاددهی آماده می‌سازد.

جدا نگه داشتن این مسئولیت‌ها باعث می‌شود نگهداری پروژه ساده‌تر باشد و بتوان منبع داده یا مراحل آماده‌سازی را بدون وابستگی مستقیم به منطق پیشنهاددهی تغییر داد.

~~~mermaid
flowchart LR
    A[ CSV فایل های خام ] --> B[بارگذاری داده]
    B --> C[ارزیابی داده]
    B --> D[پیش پردازش داده]
    C --> E[گزارش‌های کیفیت داده]
    D --> F[داده‌های آماده]
    F --> G[ماژول‌های پیشنهاددهی]
~~~

### داده‌های ورودی

پروژه انتظار دارد دو فایل زیر داخل <code>data/raw/</code> قرار داشته باشند:

| فایل | ستون‌های اصلی | کاربرد |
| --- | --- | --- |
| <code>movies.csv</code> | <code>movieId</code>، <code>title</code>، <code>genres</code> | اطلاعات فیلم‌ها |
| <code>ratings.csv</code> | <code>userId</code>، <code>movieId</code>، <code>rating</code>، <code>timestamp</code> | سابقه‌ی تعامل کاربران با فیلم‌ها |

به‌دلیل حجم داده، فایل‌های خام با Git LFS در مخزن نگهداری می‌شوند.

### اجزای اصلی

- <code>src/data/loader.py</code> خام را می‌خواند و اگر فایل موردنیاز وجود نداشته باشد، خطای واضحی ایجاد می‌کند CSV فایل های
- <code>src/data/validator.py</code> تعداد سطر و ستون، نوع داده‌ها، مقادیر خالی و رکوردهای تکراری را بررسی می‌کند
- <code>src/data/preprocessor.py</code> داده‌ی فیلم‌ها و امتیازها را برای استفاده‌ی ماژول‌های پیشنهاددهی آماده می‌کند

### ساختار پروژه

درخت زیر فایل‌هایی را نشان می‌دهد که در حال حاضر برای ماژول داده استفاده می‌شوند:

~~~text
src/
└── data/
    ├── loader.py
    ├── validator.py
    └── preprocessor.py

scripts/
└── dataset/
    ├── analyze_dataset.py
    ├── preprocess_dataset.py
    └── validate_dataset.py
~~~

### خروجی‌ها

اسکریپت‌های مربوط به داده، گزارش‌ها را در ساختار زیر ایجاد می‌کنند:

~~~text
outputs/
└── dataset_analysis/
    └── reports/
        ├── dataset_summary.txt
        ├── preprocessing_report.txt
        └── validation_report.txt
~~~

### پیش‌پردازش

برای داده‌ی فیلم‌ها، این مراحل انجام می‌شود:

1. سال انتشار از عنوان فیلم جدا می‌شود؛
2. سال انتشار از عنوان نمایشی فیلم حذف می‌شود؛
3. رشته‌ی ژانرها که با علامت <code>|</code> جدا شده است، به یک فهرست تبدیل می‌شود.

برای داده‌ی امتیازها، ستون <code>timestamp</code> در مرحله‌ی آماده‌سازی حذف می‌شود؛ چون مدل‌های فعلی هنوز از اطلاعات زمانی استفاده نمی‌کنند.

### اجرای اسکریپت‌های مربوط به داده

این دستورها را از ریشه‌ی مخزن اجرا کنید:

~~~bash
python scripts/dataset/analyze_dataset.py
python scripts/dataset/validate_dataset.py
python scripts/dataset/preprocess_dataset.py
~~~

گزارش‌های تولیدشده، اطلاعات اولیه‌ی داده، نتیجه‌ی اعتبارسنجی و تغییرات انجام‌شده در مرحله‌ی پیش‌پردازش را نشان می‌دهند.

### اصل طراحی

این لایه بر اساس جداسازی مسئولیت‌ها ساخته شده است:

- بخش بارگذاری، داده را می‌خواند؛
- بخش اعتبارسنجی، کیفیت داده را بررسی می‌کند؛
- بخش پیش‌پردازش، داده را برای مدل‌ها آماده می‌سازد.

به همین دلیل، آماده‌سازی داده از الگوریتم‌های پیشنهاددهی مستقل باقی می‌ماند.


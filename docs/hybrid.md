# Hybrid Recommendation

[🇺🇸 English](#english) | [🇮🇷 فارسی](#persian)

<a id="english"></a>

## 🇺🇸 English

### Overview

The Hybrid module coordinates the Content-Based and Collaborative recommenders. It does not train a new model and does not directly combine their scores into one normalized value. Instead, it compares their Top-N lists and presents the relationship between them in separate sections.

~~~mermaid
flowchart TD
    A[Seed movie or movies] --> B[Content-Based recommender]
    U[User ID and ratings] --> C[Collaborative recommender]
    B --> D[Content-Based candidates]
    C --> E[Collaborative candidates]
    D --> F[Remove seen movies]
    E --> F
    F --> G{Shared movie?}
    G -->|Yes| H[Special section]
    G -->|Content only| I[Content-Based section]
    G -->|Collaborative only| J[Collaborative section]
~~~

### Recommendation Flow

For each request, the Hybrid coordinator:

1. validates the movies, ratings, genre matrix, user ID, seed movie IDs, and requested Top-N size;
2. asks the Content-Based recommender for candidates from one or more seed movies;
3. asks the Collaborative recommender for candidates for the selected user;
4. removes movies already seen by that user;
5. finds the intersection between the two candidate lists;
6. returns three separate result sections.

### Result Sections

| Section | Meaning |
| --- | --- |
| <code>special</code> | Movies recommended by both models |
| <code>content_based</code> | Movies recommended only by the Content-Based model |
| <code>collaborative</code> | Movies recommended only by the Collaborative model |

Each result keeps the relevant source information, such as similarity, estimated rating, and source rank. For shared movies, the sum of the two source ranks is used only to order the <code>special</code> section. The model scores are not combined directly.

### Project Structure

The following tree shows the files currently used by the Hybrid module:

~~~text
src/
└── hybrid/
    ├── recommender.py
    ├── evaluator.py
    └── evaluate_hybrid.py

scripts/
└── hybrid/
    ├── run_hybrid.py
    └── evaluate_hybrid.py
~~~

### Outputs

The current Hybrid pipeline generates recommendation files and reports in the following structure:

~~~text
outputs/
└── hybrid/
    ├── recommendations/
    │   ├── user_5_special_recommendations.csv
    │   ├── user_5_content_recommendations.csv
    │   ├── user_5_collaborative_recommendations.csv
    │   └── user_5_all_recommendations.csv
    │
    └── reports/
        ├── user_5_hybrid_report.txt
        └── user_5_hybrid_evaluation_report.txt
~~~

The user prefix follows the user configured in the execution script.

### Multiple Seed Movies

The current implementation accepts either one movie ID or a list of movie IDs. When multiple seed movies are provided, the Content-Based module creates an average genre profile and the Hybrid coordinator uses the resulting candidates together with the Collaborative recommendations.

The execution script resolves configured movie titles to IDs before starting the Hybrid recommendation flow.

### Evaluation

The Hybrid evaluator checks the generated sections independently and together. It reports:

- recommendation counts and unique movies;
- overlap between Content-Based and Collaborative candidates;
- average source scores when available;
- genre diversity;
- duplicate IDs, missing metadata, invalid categories, and special-section overlap violations.

### Running the Pipeline

Run the Hybrid generation script from the repository root:

~~~bash
python scripts/hybrid/run_hybrid.py
~~~

After the recommendation files are generated, run the current evaluator:

~~~bash
python src/hybrid/evaluate_hybrid.py
~~~

Hybrid runtime results are written under <code>outputs/hybrid/</code>. Hybrid examples have not been added to <code>outputs/showcase/</code> yet; the showcase currently presents the dataset, Content-Based, and Collaborative stages separately.

<a id="persian"></a>

## 🇮🇷 راهنمای فارسی

### معرفی

ماژول Hybrid، سیستم‌های پیشنهاددهی Content-Based و Collaborative را در کنار هم هماهنگ می‌کند. این بخش در وضعیت فعلی مدل جدیدی آموزش نمی‌دهد و امتیازهای دو مدل را مستقیماً به یک امتیاز نهایی تبدیل نمی‌کند. وظیفه‌ی آن این است که دو فهرست Top-N را مقایسه کند و رابطه‌ی میان آن‌ها را در چند بخش جداگانه نمایش دهد.

~~~mermaid
flowchart TD
    A[یک یا چند فیلم اولیه] --> B[Content-Based پیشنهاددهنده‌ی]
    U[شناسه‌ی کاربر و داده‌ی امتیازها] --> C[Collaborative پیشنهاددهنده‌ی]
    B --> D[Content-Based نامزدهای]
    C --> E[Collaborative نامزدهای]
    D --> F[حذف فیلم‌های دیده‌شده]
    E --> F
    F --> G{فیلم مشترک است؟}
    G -->|بله| H[Special بخش]
    G -->|فقط محتوایی| I[Content-Based بخش]
    G -->|فقط مشارکتی| J[Collaborative بخش]
~~~

### روند پیشنهاددهی

برای هر درخواست، هماهنگ‌کننده‌ی Hybrid این مراحل را انجام می‌دهد:

1. اطلاعات فیلم‌ها، امتیازها، ماتریس ژانرها، شناسه‌ی کاربر، شناسه‌ی فیلم‌های اولیه و تعداد پیشنهادها را بررسی می‌کند؛
2. از پیشنهاددهنده‌ی Content-Based برای یک یا چند فیلم اولیه، گزینه‌های پیشنهادی را می‌گیرد؛
3. از پیشنهاددهنده‌ی Collaborative برای کاربر انتخاب‌شده، گزینه‌های پیشنهادی را می‌گیرد؛
4. فیلم‌هایی را که کاربر قبلاً دیده یا به آن‌ها امتیاز داده است، حذف می‌کند؛
5. فیلم‌های مشترک دو فهرست را پیدا می‌کند؛
6. نتیجه را در سه بخش جداگانه برمی‌گرداند.

### بخش‌های خروجی

| بخش | معنی |
| --- | --- |
| <code>special</code> | فیلم‌هایی که هر دو مدل پیشنهاد داده‌اند |
| <code>content_based</code> | پیشنهاد داده است Content-Based فیلم هایی که فقط مدل |
| <code>collaborative</code> | پیشنهاد داده است Collaborative فیلم هایی که فقط مدل |


هر نتیجه اطلاعات مربوط به منبع خود، مانند similarity، امتیاز تخمینی و رتبه‌ی مدل را حفظ می‌کند. برای مرتب کردن بخش <code>special</code> فقط مجموع رتبه‌های دو مدل استفاده می‌شود و امتیازهای آن‌ها مستقیماً با هم جمع نمی‌شوند.

### ساختار پروژه

درخت زیر فایل‌هایی را نشان می‌دهد که در حال حاضر برای ماژول پیشنهاددهی Hybrid استفاده می‌شوند:

~~~text
src/
└── hybrid/
    ├── recommender.py
    ├── evaluator.py
    └── evaluate_hybrid.py

scripts/
└── hybrid/
    ├── run_hybrid.py
    └── evaluate_hybrid.py
~~~

### خروجی‌ها

Pipeline مربوط به Hybrid، فایل‌های پیشنهاد و گزارش‌ها را در ساختار زیر ایجاد می‌کند:

~~~text
outputs/
└── hybrid/
    ├── recommendations/
    │   ├── user_5_special_recommendations.csv
    │   ├── user_5_content_recommendations.csv
    │   ├── user_5_collaborative_recommendations.csv
    │   └── user_5_all_recommendations.csv
    │
    └── reports/
        ├── user_5_hybrid_report.txt
        └── user_5_hybrid_evaluation_report.txt
~~~

پیشوند <code>user_5</code> بر اساس شناسه‌ی کاربری تنظیم‌شده در اسکریپت فعلی است.

### پشتیبانی از چند فیلم اولیه

پیاده‌سازی فعلی یک شناسه‌ی فیلم یا فهرستی از شناسه‌های فیلم را می‌پذیرد. اگر چند فیلم اولیه وارد شود، ماژول Content-Based میانگین ویژگی‌های ژانری آن‌ها را به‌عنوان پروفایل سلیقه می‌سازد و نتیجه را در کنار پیشنهادهای Collaborative قرار می‌دهد.

اسکریپت اجرا، عنوان‌های فیلمی را که در تنظیمات مشخص شده‌اند به شناسه‌ی فیلم تبدیل می‌کند و سپس فرایند پیشنهاددهی Hybrid را شروع می‌کند.

### ارزیابی

ارزیاب Hybrid بخش‌های خروجی را هم به‌صورت جداگانه و هم در کنار یکدیگر بررسی می‌کند. این ارزیابی شامل موارد زیر است:

- تعداد پیشنهادها و تعداد فیلم‌های یکتا؛
- میزان اشتراک نامزدهای Content-Based و Collaborative؛
- میانگین امتیازهای موجود در خروجی؛
- تنوع ژانرها؛
- شناسه‌های تکراری، اطلاعات ناقص فیلم، دسته‌بندی نامعتبر و تداخل نادرست در بخش Special.

### اجرای Pipeline

اسکریپت تولید پیشنهادهای Hybrid را از ریشه‌ی مخزن اجرا کنید:

~~~bash
python scripts/hybrid/run_hybrid.py
~~~

بعد از تولید فایل‌های پیشنهاد، ارزیاب فعلی را اجرا کنید:

~~~bash
python src/hybrid/evaluate_hybrid.py
~~~

خروجی‌های زمان اجرای Hybrid در <code>outputs/hybrid/</code> قرار می‌گیرند. نمونه‌های Hybrid هنوز داخل <code>outputs/showcase/</code> قرار نگرفته‌اند و Showcase فعلی، مراحل داده، Content-Based و Collaborative را به‌صورت جداگانه نمایش می‌دهد.


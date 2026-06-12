# SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models

## شناسنامه
- کلید BibTeX: `manakul2023selfcheckgpt`
- نوع منبع: مقاله پژوهشی / تشخیص hallucination
- سال: 2023
- نویسندگان: Potsawee Manakul, Adian Liusie, Mark J. F. Gales
- محل انتشار / ناشر: arXiv
- فایل PDF مبنا: `references/pdfs/manakul2023selfcheckgpt-2303.08896.pdf`
- وضعیت مطالعه: خلاصه‌شده

## مسئله‌ی اصلی
مدل‌های زبانی بزرگ می‌توانند پاسخ‌هایی روان ولی از نظر factuality نادرست تولید کنند. بسیاری از روش‌های fact-checking به دسترسی به احتمال‌های داخلی مدل، پایگاه دانش خارجی یا pipeline پیچیده نیاز دارند؛ اما در بسیاری از سامانه‌های واقعی، مدل به‌صورت black-box استفاده می‌شود و دسترسی به logit یا وزن مدل وجود ندارد.

## پیام محوری
SelfCheckGPT پیشنهاد می‌کند که برای تشخیص hallucination در مدل‌های black-box می‌توان چند خروجی نمونه‌برداری‌شده از همان مدل را با هم مقایسه کرد. اگر مدل درباره یک موضوع دانش پایدار داشته باشد، پاسخ‌های مختلف باید از نظر factual content سازگار باشند؛ اما اگر بخشی از پاسخ hallucinated باشد، نمونه‌های مختلف احتمالاً ناسازگاری و تناقض نشان می‌دهند.

## ارتباط با معماری نرم‌افزار
این منبع برای معماری سامانه‌های GenAI مهم است چون hallucination detection را به یک کنترل runtime یا evaluation pipeline تبدیل می‌کند. در محصول واقعی، می‌توان SelfCheckGPT را به‌عنوان یک لایه quality gate، post-generation validator یا بخشی از offline evaluation استفاده کرد؛ البته با هزینه‌ی latency و token بیشتر، چون چند بار sampling لازم دارد.

## چالش‌های معماری استخراج‌شده

| چالش | لایه‌ی درگیر | ویژگی کیفی اثرپذیر | پیامد معماری | شاهد از منبع |
|---|---|---|---|---|
| hallucination در خروجی مدل | Generation / Quality | صحت، اعتمادپذیری | نیاز به validator مستقل از مدل اصلی | مقاله روش تشخیص factual inconsistency را پیشنهاد می‌کند |
| نبود دسترسی به logit یا مدل داخلی | Integration / Serving | portability، قابلیت اجرا | روش باید black-box و API-friendly باشد | SelfCheckGPT بدون external database و بدون logit کار می‌کند |
| هزینه چندباره‌سازی inference | Runtime / Cost | latency، هزینه | باید sampling budget و مسیر async/offline طراحی شود | روش بر چند نمونه خروجی متکی است |
| تشخیص جمله‌های غیرواقعی | Evaluation | observability، debuggability | نیاز به sentence-level scoring و گزارش خطا | مقاله sentence-level hallucination detection را ارزیابی می‌کند |
| نبود ground truth در تولید آزاد | QA / Evaluation | ارزیابی‌پذیری | consistency بین نمونه‌ها به‌عنوان proxy استفاده می‌شود | ایده اصلی روش بر self-consistency بنا شده است |

## راهکارها و تاکتیک‌های پیشنهادی

| راهکار / تاکتیک | مسئله‌ای که حل می‌کند | محدودیت | امکان استفاده در گزارش |
|---|---|---|---|
| چندبار نمونه‌برداری از مدل | کشف ناسازگاری factual | افزایش هزینه و latency | مناسب برای quality gate و offline eval |
| مقایسه consistency بین پاسخ‌ها | تشخیص احتمال hallucination | ممکن است facts نادر اما درست را جریمه کند | مناسب برای معماری validation |
| scoring در سطح جمله | pinpoint کردن بخش مشکوک | نیاز به segment کردن پاسخ | مناسب برای UI/observability |
| استفاده بدون پایگاه دانش خارجی | کاهش coupling به KB | دقت وابسته به رفتار خود مدل است | مناسب برای سیستم‌های black-box |
| اجرای async برای پاسخ‌های حساس | کنترل latency | برای همه درخواست‌ها مناسب نیست | مناسب برای مسیرهای high-risk |

## معیارها و شاخص‌های ارزیابی

- معیار: AUC-PR در تشخیص factual / non-factual sentence
- کاربرد: سنجش کیفیت تشخیص hallucination در سطح جمله.
- محدودیت: وابسته به dataset و annotation انسانی است.

- معیار: passage-level factuality correlation
- کاربرد: رتبه‌بندی پاسخ‌ها بر اساس میزان factuality.
- محدودیت: یک proxy است و تضمین قطعی صحت نمی‌دهد.

- معیار: sampling count و هزینه inference
- کاربرد: تعیین بودجه عملیاتی برای validator.
- محدودیت: افزایش تعداد نمونه‌ها هزینه و latency را بالا می‌برد.

## کیفیت و محدودیت منبع

- نوع شواهد: روش تجربی، ارزیابی روی WikiBio، annotation انسانی
- قوت اصلی: ارائه روش black-box و zero-resource برای hallucination detection
- ضعف اصلی: اتکا به ناسازگاری در نمونه‌ها؛ اگر مدل با اطمینان خطای یکسان تکرار کند، روش ممکن است خطا را تشخیص ندهد.
- میزان اتکا در گزارش: زیاد؛ برای بخش کیفیت، validation و safety pipeline مناسب است.

## جایگاه در گزارش نهایی

- استفاده در بخش «کنترل hallucination و factuality»
- استفاده برای توضیح post-generation validation
- استفاده برای نشان دادن trade-off بین کیفیت و latency/cost
- استفاده در بحث black-box model integration

## نکته‌های قابل نقل یا استفاده

- برای تشخیص hallucination همیشه لازم نیست پایگاه دانش خارجی داشته باشیم؛ consistency بین نمونه‌ها می‌تواند سیگنال مفیدی باشد.
- هر validator مبتنی بر sampling باید با بودجه هزینه و latency طراحی شود.
- SelfCheckGPT برای مسیرهای حساس می‌تواند به‌صورت async یا offline اجرا شود.

## جمع‌بندی نهایی برای این منبع

SelfCheckGPT یک تاکتیک معماری برای افزایش اعتمادپذیری خروجی مدل در شرایط black-box ارائه می‌دهد. این روش نشان می‌دهد که validation خروجی می‌تواند بدون دانش خارجی و فقط با مقایسه چند نمونه انجام شود، اما هزینه عملیاتی دارد و نباید به‌عنوان تضمین قطعی factuality تلقی شود. در معماری GenAI، این منبع برای طراحی لایه‌های quality gate، hallucination detector و پایش factuality بسیار قابل استفاده است.

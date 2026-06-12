# A Comprehensive Survey of Retrieval-Augmented Generation (RAG): Evolution, Current Landscape and Future Directions

## شناسنامه
- کلید BibTeX: `gupta2024ragComprehensiveSurvey`
- نوع منبع: مقاله‌ی پیمایشی / Survey
- سال: 2024
- نویسندگان: Gupta و همکاران
- محل انتشار / ناشر: arXiv
- فایل PDF مبنا: `references/pdfs/gupta2024ragComprehensiveSurvey-2410.12837.pdf`
- وضعیت مطالعه: خلاصه‌شده

## مسئله‌ی اصلی
این منبع مسئله‌ی تولید پاسخ با اتکا به دانش بیرونی را از زاویه‌ی RAG بررسی می‌کند. مسئله‌ی اصلی این است که LLM به‌تنهایی برای دانش به‌روز، قابل‌ردیابی و دامنه‌محور کافی نیست و باید با سامانه‌ی بازیابی، نمایه‌سازی، رتبه‌بندی و ترکیب پاسخ همراه شود.

## پیام محوری
RAG یک تکنیک ساده‌ی «جست‌وجو سپس پاسخ» نیست؛ یک معماری چندلایه است که کیفیت آن به طراحی ingestion، chunking، embedding، retrieval، reranking، prompt composition، generation و evaluation وابسته است.

## ارتباط با معماری نرم‌افزار
این مقاله مستقیماً برای طراحی معماری سرویس‌های GenAI کاربرد دارد. RAG مرز میان سیستم اطلاعاتی سنتی و LLM را می‌سازد و باعث می‌شود تصمیم‌های معماری درباره‌ی داده، index، freshness، observability، security و evaluation اهمیت پیدا کنند.

## چالش‌های معماری استخراج‌شده

| چالش | لایه‌ی درگیر | ویژگی کیفی اثرپذیر | پیامد معماری | شاهد از منبع |
|---|---|---|---|---|
| کیفیت بازیابی | retrieval و vector store | درستی، قابلیت اعتماد | نیاز به طراحی chunking، embedding و reranking | مقاله اجزای RAG و تحول آن‌ها را در چرخه‌ی retrieval و generation بررسی می‌کند. |
| تازگی و همگام‌سازی دانش | ingestion و index | تازگی، سازگاری | نیاز به pipeline به‌روزرسانی و versioning index | منبع RAG را راهی برای اتصال مدل به دانش بیرونی و قابل‌به‌روزرسانی می‌داند. |
| خطای ترکیب زمینه و پاسخ | prompt/generation | faithfulness، explainability | نیاز به citation، context filtering و پاسخ محدود به منبع | مقاله بر تعامل میان بازیابی و تولید پاسخ تأکید دارد. |
| ارزیابی چندمرحله‌ای RAG | evaluation | آزمون‌پذیری، مشاهده‌پذیری | نیاز به ارزیابی retrieval و generation به‌صورت جداگانه | منبع landscape روش‌ها و جهت‌های آینده‌ی RAG را مرور می‌کند. |

## راهکارها و تاکتیک‌های پیشنهادی

| راهکار / تاکتیک | مسئله‌ای که حل می‌کند | محدودیت | امکان استفاده در گزارش |
|---|---|---|---|
| pipeline مستقل برای ingestion و indexing | مدیریت دانش بیرونی | پیچیدگی عملیاتی دارد | مناسب برای معماری مرجع RAG |
| reranking و filtering قبل از generation | کاهش زمینه‌ی نامرتبط | هزینه و latency را افزایش می‌دهد | مناسب برای بخش کیفیت بازیابی |
| citation و grounded answer | کاهش hallucination | نیاز به کنترل دقیق context دارد | مناسب برای بخش trustworthiness |
| ارزیابی جداگانه‌ی retrieval و generation | تشخیص محل خطا | نیاز به داده‌ی benchmark دارد | مناسب برای فصل ارزیابی |

## معیارها و شاخص‌های ارزیابی

- معیار: recall@k، precision@k، MRR، faithfulness، answer relevance، context relevance، citation accuracy
- کاربرد: تشخیص اینکه خطا از بازیابی، رتبه‌بندی، context selection یا generation آمده است.
- محدودیت: ارزیابی RAG به داده‌ی دامنه‌محور و نمونه‌های پرسش/پاسخ معتبر نیاز دارد.

## کیفیت و محدودیت منبع

- نوع شواهد: survey جامع
- قوت اصلی: ارائه‌ی نگاه معماری به اجزای RAG و جهت‌های آینده‌ی آن
- ضعف اصلی: به‌دلیل survey بودن، جزئیات implementation و trade-offهای عملی هر ابزار را کامل حل نمی‌کند.
- میزان اتکا در گزارش: زیاد، برای بخش معماری RAG و pipeline دانش

## جایگاه در گزارش نهایی

- بخش معماری RAG
- بخش data/index lifecycle
- بخش evaluation و observability در سامانه‌های GenAI
- بخش کاهش hallucination با grounding

## نکته‌های قابل نقل یا استفاده

- RAG کیفیت مدل را به کیفیت داده و retrieval وابسته می‌کند.
- شکست RAG را باید مرحله‌ای تحلیل کرد، نه فقط به خروجی مدل نسبت داد.
- در production، RAG بدون پایش index، freshness و معیارهای ارزیابی ناقص است.

## جمع‌بندی نهایی برای این منبع

این منبع نشان می‌دهد RAG یک سبک معماری برای اتصال LLM به دانش بیرونی است. ارزش آن برای گزارش در این است که RAG را به‌عنوان مجموعه‌ای از تصمیم‌های معماری درباره‌ی داده، بازیابی، ارزیابی، اعتمادپذیری و عملیات معرفی می‌کند، نه صرفاً یک الگوی prompt engineering.

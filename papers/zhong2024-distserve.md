# DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving

## شناسنامه
- کلید BibTeX: `zhong2024distserve`
- نوع منبع: مقاله پژوهشی / معماری serving برای مدل‌های زبانی بزرگ
- سال: 2024
- نویسندگان: Yinmin Zhong و همکاران
- محل انتشار / ناشر: arXiv
- وضعیت مطالعه: خلاصه‌شده
- فایل PDF مبنا: `references/pdfs/zhong2024distserve-2401.09670.pdf`

## مسئله‌ی اصلی
Serving مدل‌های زبانی بزرگ از دو فاز متفاوت تشکیل می‌شود: prefill برای پردازش prompt و تولید اولین token، و decoding برای تولید tokenهای بعدی. بسیاری از سیستم‌ها این دو فاز را روی منابع مشترک اجرا می‌کنند، در حالی که الگوی مصرف منابع، حساسیت latency و معیارهای SLO در این دو فاز متفاوت است. نتیجه این هم‌مکانی، interference و کاهش goodput در بارهای واقعی است.

## پیام محوری
DistServe نشان می‌دهد که جداسازی فاز prefill و decoding می‌تواند یک تصمیم معماری مهم برای بهینه‌سازی goodput باشد. این مقاله به‌جای نگاه کلی به latency، TTFT و TPOT را جدا می‌کند و resource allocation را متناسب با هر فاز انجام می‌دهد.

## ارتباط با معماری نرم‌افزار
این منبع برای بخش «معماری serving و performance engineering در GenAI» مهم است. در معماری سرویس‌های LLM، زمان پاسخ فقط یک عدد واحد نیست؛ time to first token و time per output token دو ویژگی رفتاری جدا هستند. بنابراین طراحی scheduling، تخصیص GPU، batching و network placement باید بر اساس این تفکیک انجام شود.

## چالش‌های معماری استخراج‌شده

| چالش | لایه‌ی درگیر | ویژگی کیفی اثرپذیر | پیامد معماری | شاهد از منبع |
|---|---|---|---|---|
| interference بین prefill و decoding | inference serving | latency، throughput | colocating دو فاز باعث افت goodput می‌شود | تحلیل prefill-decoding interference |
| SLOهای متفاوت برای TTFT و TPOT | performance management | پاسخ‌گویی، تجربه کاربر | یک سیاست scheduling واحد کافی نیست | تفکیک TTFT و TPOT در مسئله |
| تخصیص منابع ناهمگون | resource management | هزینه، مقیاس‌پذیری | هر فاز به الگوی parallelism و GPU allocation جدا نیاز دارد | co-optimization منابع برای هر فاز |
| هزینه ارتباط بین فازها | cluster architecture | latency، کارایی | disaggregation نیازمند توجه به bandwidth و placement است | placement براساس bandwidth کلاستر |
| بهینه‌سازی goodput تحت constraint | operations | کارایی اقتصادی | throughput خام معیار کافی نیست | تعریف goodput در چارچوب محدودیت latency |

## راهکارها و تاکتیک‌های پیشنهادی

| راهکار / تاکتیک | مسئله‌ای که حل می‌کند | محدودیت | امکان استفاده در گزارش |
|---|---|---|---|
| جداسازی prefill و decoding | کاهش interference | نیازمند شبکه و هماهنگی بین GPUها | بالا |
| تعریف TTFT و TPOT به‌عنوان SLO جدا | ابهام در latency | پیچیدگی مانیتورینگ بیشتر | بالا |
| تخصیص منابع اختصاصی برای هر فاز | ناکارایی resource sharing | ممکن است در بار کم over-provision شود | متوسط تا بالا |
| placement آگاه از bandwidth | هزینه ارتباط بین فازها | وابسته به topology کلاستر | متوسط |
| goodput-oriented scheduling | تمرکز روی درخواست‌های SLO-satisfied | نیازمند مدل‌سازی دقیق workload | بالا |

## معیارها و شاخص‌های ارزیابی

- معیار: TTFT، TPOT، goodput، نرخ درخواست‌های داخل SLO، utilization GPU
- کاربرد: طراحی و ارزیابی inference platform برای محصولات GenAI با workload تعاملی
- محدودیت: نتایج به مدل، طول prompt، طول خروجی، شبکه کلاستر و الگوی ترافیک وابسته است.

## کیفیت و محدودیت منبع

- نوع شواهد: طراحی سیستم و ارزیابی تجربی
- قوت اصلی: تبدیل serving LLM از مسئله throughput خام به مسئله goodput تحت SLO
- ضعف اصلی: تمرکز روی serving است و به لایه‌های محصولی مانند کیفیت پاسخ، امنیت یا RAG کمتر می‌پردازد.
- میزان اتکا در گزارش: بالا برای performance architecture و inference serving

## جایگاه در گزارش نهایی

- قابل استفاده در بخش serving architecture
- مناسب برای توضیح trade-off بین latency، هزینه و GPU allocation
- مفید برای بخش ویژگی‌های کیفی، به‌ویژه performance، scalability و cost efficiency

## نکته‌های قابل نقل یا استفاده

- در LLM serving، latency باید به TTFT و TPOT شکسته شود.
- goodput معیار معماری بهتری از throughput خام برای workloadهای SLO-driven است.
- جداسازی فازهای inference می‌تواند یک تاکتیک معماری برای کاهش interference باشد.

## جمع‌بندی نهایی برای این منبع

DistServe یک منبع مهم برای تحلیل معماری inference serving است. پیام اصلی آن این است که LLM serving باید بر اساس رفتار متفاوت فازهای prefill و decoding طراحی شود؛ در غیر این صورت، سیستم با وجود مصرف زیاد GPU ممکن است نتواند SLOهای کاربرمحور را برآورده کند.

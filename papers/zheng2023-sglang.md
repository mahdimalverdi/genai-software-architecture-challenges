# SGLang: Efficient Execution of Structured Language Model Programs

## شناسنامه
- کلید BibTeX: `zheng2023sglang`
- نوع منبع: مقاله پژوهشی / سیستم اجرای برنامه‌های مبتنی بر مدل زبانی
- سال: 2023
- نویسندگان: Lianmin Zheng و همکاران
- محل انتشار / ناشر: arXiv
- وضعیت مطالعه: خلاصه‌شده
- فایل PDF مبنا: `references/pdfs/zheng2023sglang-2312.07104.pdf`

## مسئله‌ی اصلی
برنامه‌های مبتنی بر مدل زبانی معمولاً فقط یک فراخوانی ساده به مدل نیستند؛ آن‌ها شامل چند مرحله تولید، کنترل جریان، few-shot prompting، خروجی ساخت‌یافته، گفت‌وگوی چندمرحله‌ای، RAG و گاهی agent control هستند. اجرای این برنامه‌ها با API یا runtimeهای عادی باعث تکرار محاسبه، استفاده ناکارا از KV cache، latency بالا و کاهش throughput می‌شود.

## پیام محوری
SGLang نشان می‌دهد که برای ساخت سامانه‌های GenAI پیچیده، فقط مدل مهم نیست؛ زبان برنامه‌نویسی و runtime اجرای orchestration نیز یک جزء معماری مستقل‌اند. این مقاله SGLang را به‌عنوان ترکیبی از یک زبان front-end برای بیان برنامه‌های LLM و یک runtime برای اجرای بهینه آن‌ها معرفی می‌کند.

## ارتباط با معماری نرم‌افزار
این منبع برای بخش «معماری اجرای سرویس‌های GenAI» مهم است. در معماری سامانه‌های GenAI، لایه orchestration و لایه inference serving باید با هم دیده شوند، چون تصمیم‌های سطح برنامه، مانند branching، parallel generation و constrained decoding، مستقیماً روی latency، throughput، مصرف GPU و reuse شدن cache اثر می‌گذارند.

## چالش‌های معماری استخراج‌شده

| چالش | لایه‌ی درگیر | ویژگی کیفی اثرپذیر | پیامد معماری | شاهد از منبع |
|---|---|---|---|---|
| اجرای چندمرحله‌ای برنامه‌های LLM | orchestration / runtime | کارایی، latency | API ساده برای workflowهای پیچیده کافی نیست | معرفی front-end زبان SGLang |
| تکرار محاسبه در promptهای مشترک | inference runtime | throughput، هزینه | نیاز به reuse در KV cache و prefix sharing | RadixAttention برای reuse کردن KV cache |
| خروجی ساخت‌یافته | decoding / validation | درستی، قابلیت اتکا | JSON و قالب‌های محدودشده نیازمند constrained decoding هستند | compressed finite state machines برای structured decoding |
| اجرای موازی شاخه‌های تولید | orchestration | latency، مقیاس‌پذیری | معماری باید parallelism را در سطح برنامه پشتیبانی کند | primitives مربوط به parallel control |
| وابستگی معماری برنامه به runtime | platform architecture | maintainability، portability | انتخاب runtime بخشی از تصمیم معماری محصول می‌شود | ترکیب زبان front-end و runtime در SGLang |

## راهکارها و تاکتیک‌های پیشنهادی

| راهکار / تاکتیک | مسئله‌ای که حل می‌کند | محدودیت | امکان استفاده در گزارش |
|---|---|---|---|
| جداسازی زبان برنامه از runtime | پیچیدگی orchestration | نیازمند پذیرش چارچوب خاص | بالا |
| RadixAttention | تکرار KV cache در promptهای مشترک | بیشتر برای workloadهای دارای prefix مشترک مفید است | بالا |
| constrained decoding بهینه | خروجی ساخت‌یافته کند یا ناپایدار | نیازمند تعریف grammar یا schema | بالا |
| primitives برای parallelism | کندی برنامه‌های چندشاخه | پیچیدگی کنترل منابع | متوسط |
| runtime-aware design | ناهماهنگی برنامه و serving | وابستگی به platform | بالا |

## معیارها و شاخص‌های ارزیابی

- معیار: throughput، latency، سرعت اجرای برنامه‌های multi-call، کارایی KV cache reuse
- کاربرد: ارزیابی runtimeهای serving و orchestration برای سامانه‌های GenAI
- محدودیت: نتایج به نوع workload، مدل، طول prompt، shared prefix و سخت‌افزار وابسته است.

## کیفیت و محدودیت منبع

- نوع شواهد: طراحی سیستم و ارزیابی تجربی
- قوت اصلی: نشان دادن رابطه مستقیم بین زبان برنامه‌نویسی GenAI و runtime inference
- ضعف اصلی: تمرکز اصلی بر کارایی است و کمتر به جنبه‌هایی مانند governance، امنیت و lifecycle پرداخته می‌شود.
- میزان اتکا در گزارش: بالا برای بخش runtime و serving، متوسط برای بحث‌های عمومی معماری

## جایگاه در گزارش نهایی

- قابل استفاده در بخش معماری اجرای برنامه‌های LLM
- قابل استفاده در بحث inference serving و orchestration
- مناسب برای نشان دادن اینکه GenAI service فقط prompt engineering نیست و به runtime architecture نیاز دارد.

## نکته‌های قابل نقل یا استفاده

- برنامه‌های GenAI پیچیده نیازمند abstraction و runtime اختصاصی هستند.
- KV cache reuse می‌تواند به یک تاکتیک معماری برای کاهش هزینه و latency تبدیل شود.
- constrained decoding باید در معماری خروجی‌های ساخت‌یافته دیده شود.

## جمع‌بندی نهایی برای این منبع

SGLang یک منبع کلیدی برای توضیح لایه runtime در معماری نرم‌افزارهای GenAI است. پیام اصلی آن این است که با پیچیده شدن کاربردهای LLM، معماری باید میان منطق برنامه، orchestration و inference runtime پیوند صریح برقرار کند؛ در غیر این صورت latency، هزینه و پیچیدگی عملیاتی به‌سرعت افزایش می‌یابد.

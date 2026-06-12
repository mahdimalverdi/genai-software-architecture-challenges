# Taming the Titans: A Survey of Efficient LLM Inference Serving

## شناسنامه

- کلید BibTeX: `zhen2025tamingTitans`
- نوع منبع: مقاله‌ی مروری / survey
- سال: 2025
- نویسندگان: Ranran Zhen، Juntao Li، Yixin Ji، Zhenlin Yang، Tong Liu، Qingrong Xia، Xinyu Duan، Zhefeng Wang، Baoxing Huai، Min Zhang
- محل انتشار / ناشر: arXiv
- فایل PDF مبنا: `references/pdfs/zhen2025tamingTitans-2504.19720.pdf`
- وضعیت مطالعه: خلاصه‌شده

## مسئله‌ی اصلی

این منبع مسئله‌ی serving و بهره‌برداری از مدل‌های زبانی بزرگ را از زاویه‌ی کارایی، تأخیر، throughput و استفاده‌ی بهینه از GPU بررسی می‌کند. مسئله‌ی اصلی این است که LLMها به‌خاطر تعداد زیاد پارامترها و هزینه‌ی attention، در زمان inference فشار زیادی به حافظه و محاسبات وارد می‌کنند. بنابراین، کیفیت معماری سرویس فقط به مدل وابسته نیست؛ بلکه به چگونگی placement مدل، زمان‌بندی درخواست‌ها، مدیریت KV cache، توزیع بار، disaggregation و طراحی سطح cluster وابسته است.

## پیام محوری

پیام محوری مقاله این است که LLM inference serving یک مسئله‌ی معماری و عملیاتی مستقل است، نه فقط اجرای یک مدل روی GPU. برای رسیدن به latency پایین، throughput بالا و هزینه‌ی قابل کنترل، باید تصمیم‌های سطح instance، سطح cluster و سناریوهای کاربردی با هم دیده شوند.

## ارتباط با معماری نرم‌افزار

این مقاله برای معماری نرم‌افزار مهم است چون بخش inference را به‌عنوان یک زیردامنه‌ی معماری معرفی می‌کند. در سرویس‌های GenAI، انتخاب engine، سیاست batching، مدیریت حافظه، load balancing، GPU placement و جداسازی prefill/decode مستقیماً روی ویژگی‌های کیفی مثل کارایی، مقیاس‌پذیری، هزینه، دسترس‌پذیری و قابلیت عملیات اثر می‌گذارند. این منبع کمک می‌کند بخش «مدل و inference» گزارش فقط در سطح مدل باقی نماند و به معماری serving برسد.

## چالش‌های معماری استخراج‌شده

| چالش | لایه‌ی درگیر | ویژگی کیفی اثرپذیر | پیامد معماری | شاهد از منبع |
|---|---|---|---|---|
| سربار حافظه‌ی مدل و KV cache | inference و serving | کارایی، هزینه، مقیاس‌پذیری | نیاز به storage management، cache policy و memory-aware scheduling | بحث instance-level serving |
| نوسان طول خروجی و زمان decode | زمان‌بندی درخواست | latency، throughput | batching و scheduling باید پویا و وابسته به طول درخواست باشد | decoding length prediction و request scheduling |
| استفاده‌ی ناکارا از GPU | زیرساخت و deployment | هزینه، کارایی | معماری باید placement، load balancing و resource sharing را کنترل کند | model placement و cluster deployment |
| تفاوت نیاز prefill و decode | serving pipeline | latency، throughput | جداسازی مراحل می‌تواند به تصمیم معماری برای disaggregation تبدیل شود | disaggregation paradigm |
| مقیاس‌پذیری در سطح cluster | عملیات و زیرساخت | دسترس‌پذیری، مقیاس‌پذیری | سرویس باید چند instance، چند GPU و سیاست توزیع بار داشته باشد | cluster-level strategies |

## راهکارها و تاکتیک‌های پیشنهادی

| راهکار / تاکتیک | مسئله‌ای که حل می‌کند | محدودیت | امکان استفاده در گزارش |
|---|---|---|---|
| model placement آگاه از منابع | کاهش جابه‌جایی و مصرف حافظه | وابسته به topology و workload | زیاد؛ بخش inference |
| request scheduling و continuous batching | افزایش throughput و کاهش idle GPU | پیچیدگی در fairness و tail latency | زیاد؛ بخش کارایی |
| KV cache management | کنترل مصرف حافظه | trade-off میان حافظه و latency | زیاد؛ بخش هزینه و مقیاس‌پذیری |
| prefill/decode disaggregation | بهینه‌سازی مراحل متفاوت inference | نیازمند زیرساخت پیچیده‌تر | متوسط تا زیاد |
| load balancing در سطح cluster | پایداری و استفاده‌ی بهتر از GPUها | نیازمند telemetry دقیق | زیاد؛ بخش عملیات |

## معیارها و شاخص‌های ارزیابی

- معیار: latency و tail latency
- کاربرد: سنجش تجربه‌ی کاربر و زمان پاسخ در سرویس‌های تعاملی
- محدودیت: به طول prompt، طول خروجی، مدل و batching وابسته است

- معیار: throughput و tokens/sec
- کاربرد: سنجش ظرفیت سرویس و بهره‌وری GPU
- محدودیت: افزایش throughput ممکن است latency را بدتر کند

- معیار: GPU utilization و هزینه‌ی هر درخواست
- کاربرد: تحلیل اقتصادی serving
- محدودیت: در workloadهای واقعی نوسان زیادی دارد

## کیفیت و محدودیت منبع

- نوع شواهد: مروری / فنی
- قوت اصلی: دسته‌بندی منظم روش‌های efficient serving در سطح instance و cluster
- ضعف اصلی: مقاله بیشتر طبقه‌بندی روش‌هاست و یک معماری مرجع اجرایی واحد ارائه نمی‌کند
- میزان اتکا در گزارش: زیاد

## جایگاه در گزارش نهایی

- چالش‌های مدل و inference
- هزینه، کارایی و مقیاس‌پذیری
- مشاهده‌پذیری و عملیات
- نگهداشت‌پذیری و بدهی فنی

## نکته‌های قابل نقل یا استفاده

- inference serving برای LLMها یک مسئله‌ی معماری مستقل است، نه یک جزئیات پیاده‌سازی.
- تصمیم‌های batching، scheduling، placement و cache management مستقیماً ویژگی‌های کیفی را تغییر می‌دهند.
- بهینه‌سازی inference همیشه trade-off میان latency، throughput، هزینه و پیچیدگی عملیاتی است.

## جمع‌بندی نهایی برای این منبع

این منبع برای بخش inference و serving گزارش وزن زیادی دارد. مقاله نشان می‌دهد که وقتی GenAI وارد محصول واقعی می‌شود، معماری باید GPU، حافظه، زمان‌بندی، توزیع بار و هزینه را به‌عنوان بخش‌های اصلی طراحی ببیند. استفاده از این منبع در گزارش کمک می‌کند چالش‌های عملیاتی LLM از سطح مفهومی به تصمیم‌های معماری مشخص تبدیل شوند.

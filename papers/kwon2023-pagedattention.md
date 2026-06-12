# Efficient Memory Management for Large Language Model Serving with PagedAttention

## شناسنامه

- کلید BibTeX: `kwon2023pagedattention`
- نوع منبع: مقاله‌ی پژوهشی / سیستم serving
- سال: 2023
- نویسندگان: Woosuk Kwon، Zhuohan Li، Siyuan Zhuang، Ying Sheng، Lianmin Zheng، Cody Hao Yu، Joseph E. Gonzalez، Hao Zhang، Ion Stoica
- محل انتشار / ناشر: SOSP 2023 / arXiv
- فایل PDF مبنا: `references/pdfs/kwon2023pagedattention-2309.06180.pdf`
- وضعیت مطالعه: خلاصه‌شده

## مسئله‌ی اصلی

این مقاله مسئله‌ی مدیریت حافظه در serving مدل‌های زبانی بزرگ را بررسی می‌کند. برای throughput بالا، سامانه باید تعداد زیادی درخواست را هم‌زمان batch کند، اما KV cache هر درخواست بزرگ است و در طول تولید پاسخ به‌صورت پویا رشد و کاهش پیدا می‌کند. مدیریت ناکارآمد این حافظه باعث fragmentation و duplication می‌شود و در نهایت batch size، throughput و هزینه‌ی سرویس را محدود می‌کند.

## پیام محوری

پیام محوری مقاله این است که bottleneck اصلی در serving LLM فقط compute نیست؛ مدیریت حافظه‌ی KV cache نیز یک مسئله‌ی معماری مرکزی است. ایده‌ی PagedAttention با الهام از virtual memory و paging سیستم‌عامل، KV cache را به واحدهای قابل مدیریت تبدیل می‌کند و روی آن سیستم vLLM ساخته می‌شود.

## ارتباط با معماری نرم‌افزار

این منبع برای معماری نرم‌افزار مهم است چون نشان می‌دهد جزئیات runtime و memory management می‌توانند تصمیم‌های سطح معماری را تغییر دهند. اگر serving engine نتواند حافظه را خوب مدیریت کند، معماری حتی با GPU کافی هم به throughput مطلوب نمی‌رسد. بنابراین انتخاب runtime مثل vLLM، سیاست batching و مدیریت cache باید در بخش تصمیم‌های معماری GenAI service ثبت شود.

## چالش‌های معماری استخراج‌شده

| چالش | لایه‌ی درگیر | ویژگی کیفی اثرپذیر | پیامد معماری | شاهد از منبع |
|---|---|---|---|---|
| مصرف زیاد KV cache | inference runtime | کارایی، هزینه | معماری باید memory-aware باشد | مسئله‌ی KV cache |
| fragmentation حافظه | serving engine | throughput، مقیاس‌پذیری | batch size محدود می‌شود | تحلیل حافظه‌ی ناکارآمد |
| رشد و کاهش پویای درخواست‌ها | scheduling و batching | latency، throughput | continuous batching بدون مدیریت حافظه کافی نیست | dynamic KV cache |
| duplication در cache | runtime و memory sharing | هزینه، کارایی | نیاز به sharing و reuse در سطح engine | flexible sharing در vLLM |
| وابستگی کارایی به طول sequence | مدل و workload | پیش‌بینی‌پذیری، هزینه | benchmark باید سناریوهای long context را پوشش دهد | نتایج بهتر برای sequenceهای طولانی‌تر |

## راهکارها و تاکتیک‌های پیشنهادی

| راهکار / تاکتیک | مسئله‌ای که حل می‌کند | محدودیت | امکان استفاده در گزارش |
|---|---|---|---|
| PagedAttention | fragmentation و waste حافظه | وابسته به runtime خاص | زیاد؛ بخش inference |
| vLLM به‌عنوان serving engine | throughput و مدیریت KV cache | نیازمند سازگاری با deployment | زیاد؛ بخش معماری نمونه |
| KV cache sharing | duplication حافظه | پیچیدگی در مدیریت state | متوسط تا زیاد |
| memory-aware batching | محدودیت batch size | نیازمند telemetry دقیق | زیاد؛ بخش کارایی |
| benchmark با طول‌های مختلف sequence | ارزیابی واقع‌بینانه serving | اجرای آن پرهزینه است | متوسط |

## معیارها و شاخص‌های ارزیابی

- معیار: throughput
- کاربرد: سنجش ظرفیت serving در شرایط batch
- محدودیت: به طول prompt و output وابسته است

- معیار: latency در سطح یکسان
- کاربرد: مقایسه‌ی engineها بدون فدا کردن تجربه‌ی کاربر
- محدودیت: میانگین latency برای tail behavior کافی نیست

- معیار: میزان waste حافظه‌ی KV cache
- کاربرد: تحلیل بهره‌وری GPU memory
- محدودیت: به مدل و pattern درخواست وابسته است

## کیفیت و محدودیت منبع

- نوع شواهد: تجربی / سیستم نرم‌افزاری
- قوت اصلی: تبدیل مسئله‌ی حافظه‌ی LLM serving به راهکار اجرایی مشخص و قابل پیاده‌سازی
- ضعف اصلی: تمرکز مقاله روی runtime و serving است و همه‌ی جنبه‌های عملیاتی مانند observability و governance را پوشش نمی‌دهد
- میزان اتکا در گزارش: زیاد

## جایگاه در گزارش نهایی

- چالش‌های مدل و inference
- هزینه، کارایی و مقیاس‌پذیری
- مشاهده‌پذیری و عملیات
- نگهداشت‌پذیری و بدهی فنی

## نکته‌های قابل نقل یا استفاده

- در LLM serving، KV cache می‌تواند bottleneck اصلی معماری باشد.
- افزایش throughput بدون مدیریت حافظه‌ی هوشمند ممکن نیست.
- runtime انتخابی، مثل vLLM، یک تصمیم معماری است نه صرفاً جزئیات پیاده‌سازی.

## جمع‌بندی نهایی برای این منبع

این مقاله یکی از منابع کلیدی برای بخش inference و serving است. ارزش اصلی آن در نشان دادن این است که کارایی سرویس LLM فقط به مدل یا GPU وابسته نیست، بلکه به طراحی حافظه، batching و runtime بستگی دارد. وزن این منبع در گزارش زیاد است، مخصوصاً برای توضیح trade-offهای کارایی و هزینه.

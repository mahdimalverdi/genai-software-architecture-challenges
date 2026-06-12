# OWASP Top 10 for LLM Applications 2025

## شناسنامه
- کلید BibTeX: `owasp2025llmTop10`
- نوع منبع: راهنمای امنیتی / فهرست ریسک
- سال: ۲۰۲۵
- نویسنده / نهاد: OWASP Foundation
- محل انتشار / ناشر: OWASP GenAI Security Project
- فایل PDF مبنا در مخزن: ندارد
- وضعیت مطالعه: خلاصه‌شده

## مسئله‌ی اصلی
این منبع مهم‌ترین ریسک‌های امنیتی در کاربردهای مبتنی بر مدل‌های زبانی بزرگ را دسته‌بندی می‌کند. مسئله‌ی اصلی این است که LLM applicationها فقط با تهدیدهای سنتی نرم‌افزار مواجه نیستند؛ prompt injection، leakage، supply chain، excessive agency، insecure output handling و وابستگی به ابزارها و agentها سطح حمله‌ی تازه‌ای ایجاد می‌کنند.

در سامانه‌های GenAI، مرز میان ورودی کاربر، دستور سیستم، داده‌ی بازیابی‌شده، ابزارهای بیرونی و خروجی مدل همیشه روشن نیست. همین مسئله باعث می‌شود کنترل‌های امنیتی کلاسیک کافی نباشند.

## پیام محوری
پیام محوری منبع این است که امنیت LLM application باید در سطح معماری دیده شود. تهدیدها فقط مربوط به مدل نیستند؛ بلکه از اتصال مدل به داده، ابزار، حافظه، plugin، agent، API و خروجی‌های downstream ایجاد می‌شوند.

## ارتباط با معماری نرم‌افزار
این منبع برای گزارش نهایی از منظر security architecture بسیار کلیدی است. OWASP کمک می‌کند ریسک‌های GenAI به decisionهای معماری تبدیل شوند: جداسازی trust boundaryها، validation خروجی، محدودکردن agent، کنترل دسترسی ابزارها، policy enforcement، monitoring و sandboxing.

در گزارش می‌توان از این منبع برای تحلیل اینکه چرا GenAI به security layer مخصوص خودش نیاز دارد استفاده کرد.

## چالش‌های معماری استخراج‌شده

| چالش | لایه‌ی درگیر | ویژگی کیفی اثرپذیر | پیامد معماری | شاهد از منبع |
|---|---|---|---|---|
| prompt injection مستقیم یا غیرمستقیم | prompt، retrieval، agent | امنیت، integrity | باید ورودی‌های غیرقابل اعتماد از دستور سیستم جدا شوند | OWASP LLM Top 10 |
| افشای داده حساس | prompt، memory، logs | confidentiality، privacy | نیاز به redaction و access control | دسته‌بندی ریسک‌های LLM |
| خروجی ناامن مدل | output handling، downstream APIs | امنیت، reliability | خروجی مدل نباید مستقیم اجرا یا اعتماد شود | insecure output handling |
| excessive agency | agent، tools، permissions | safety، security | دسترسی ابزارها باید least privilege باشد | ریسک‌های agentic LLM |
| supply chain مدل و dependency | model provider، plugins، packages | integrity، resilience | باید provenance و versioning کنترل شود | ریسک supply chain |

## راهکارها و تاکتیک‌های پیشنهادی

| راهکار / تاکتیک | مسئله‌ای که حل می‌کند | محدودیت | امکان استفاده در گزارش |
|---|---|---|---|
| جداسازی trust boundary | کاهش اثر prompt injection | اجرای کامل آن در RAG دشوار است | بسیار بالا |
| output validation و sanitization | جلوگیری از اجرای خروجی خطرناک | ممکن است false positive داشته باشد | بالا |
| least privilege برای ابزارها | کنترل excessive agency | نیازمند طراحی دقیق permissionها | بسیار بالا |
| sandboxing اجرای ابزار | محدودکردن آسیب | هزینه‌ی زیرساختی و عملیاتی | متوسط تا بالا |
| monitoring و threat logging | کشف حمله و incident response | ریسک ذخیره داده حساس | بالا |
| dependency/model provenance | کنترل supply chain | نیازمند governance و tooling | بالا |

## معیارها و شاخص‌های ارزیابی

- معیار: تعداد و شدت findingهای security test
- کاربرد: سنجش ریسک‌های شناخته‌شده در application
- محدودیت: پوشش تست همیشه کامل نیست

- معیار: prompt injection success rate
- کاربرد: ارزیابی مقاومت در برابر حمله‌های prompt-based
- محدودیت: حمله‌ها با paraphrase و context جدید تغییر می‌کنند

- معیار: tool misuse rate
- کاربرد: سنجش کنترل agent و ابزارها
- محدودیت: تعریف misuse وابسته به context محصول است

- معیار: sensitive data exposure incidents
- کاربرد: سنجش محرمانگی و privacy
- محدودیت: رخدادهای پنهان ممکن است کشف نشوند

## کیفیت و محدودیت منبع

- نوع شواهد: راهنمای امنیتی و طبقه‌بندی ریسک
- قوت اصلی: تبدیل ریسک‌های LLM به زبان قابل استفاده برای طراحی و threat modeling
- ضعف اصلی: فهرست Top 10 نسخه‌بندی می‌شود و با تغییر اکوسیستم ممکن است نیاز به به‌روزرسانی داشته باشد
- میزان اتکا در گزارش: بسیار بالا برای بخش امنیت و threat model

## جایگاه در گزارش نهایی

- بخش تهدیدهای معماری در GenAI
- بخش prompt injection و agent security
- بخش کنترل خروجی و tool access
- بخش security governance و monitoring

## نکته‌های قابل نقل یا استفاده

- امنیت LLM application فقط امنیت مدل نیست؛ امنیت اتصال مدل به داده، ابزار و خروجی‌های downstream است.
- prompt injection یک ریسک معماری است، نه صرفاً یک مشکل promptنویسی.
- agentها باید با حداقل دسترسی، sandbox و logging طراحی شوند.

## جمع‌بندی نهایی برای این منبع

این منبع ستون بخش امنیت گزارش است. کمک می‌کند تهدیدهای GenAI به چالش‌های معماری ملموس تبدیل شوند و نشان می‌دهد چرا سامانه‌های مبتنی بر LLM به طراحی امنیتی متفاوت از نرم‌افزارهای سنتی نیاز دارند.

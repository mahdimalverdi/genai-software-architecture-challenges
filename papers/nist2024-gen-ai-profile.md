# Artificial Intelligence Risk Management Framework: Generative AI Profile

## شناسنامه
- کلید BibTeX: `nist2024genAiProfile`
- نوع منبع: گزارش فنی / استاندارد راهنما
- سال: ۲۰۲۴
- نویسنده / نهاد: National Institute of Standards and Technology (NIST)
- محل انتشار / ناشر: NIST AI 600-1
- فایل PDF مبنا در مخزن: ندارد
- وضعیت مطالعه: خلاصه‌شده

## مسئله‌ی اصلی
این منبع به مدیریت ریسک در سامانه‌های هوش مصنوعی مولد می‌پردازد. مسئله‌ی اصلی این است که GenAI ریسک‌هایی ایجاد می‌کند که فقط فنی نیستند: hallucination، سوءاستفاده، افشای داده، bias، تولید محتوای مضر، وابستگی به داده‌ی آموزشی، ابهام در منشأ خروجی و دشواری ارزیابی.

در نتیجه سازمانی که GenAI را وارد محصول یا فرایند می‌کند باید فراتر از accuracy و performance، ریسک را در سطح governance، طراحی، توسعه، استقرار و عملیات مدیریت کند.

## پیام محوری
پیام محوری NIST این است که GenAI باید با رویکرد risk management اداره شود. یعنی سازمان باید context استفاده، ذی‌نفعان، آسیب‌های احتمالی، کنترل‌ها، پایش، مستندسازی و accountability را از ابتدا تعریف کند.

## ارتباط با معماری نرم‌افزار
این منبع برای گزارش نهایی از منظر governance و risk architecture مهم است. در معماری GenAI، کنترل ریسک باید به componentهای واقعی تبدیل شود: policy layer، logging، monitoring، human review، data governance، content safety، red-teaming، model card، incident response و access control.

در واقع NIST کمک می‌کند بخش «ویژگی‌های کیفی» گزارش فقط روی performance و accuracy نماند و ویژگی‌هایی مثل safety، security، privacy، accountability و transparency را هم وارد تحلیل معماری کند.

## چالش‌های معماری استخراج‌شده

| چالش | لایه‌ی درگیر | ویژگی کیفی اثرپذیر | پیامد معماری | شاهد از منبع |
|---|---|---|---|---|
| خروجی نادرست یا ساختگی | generation، evaluation | صحت، اعتمادپذیری | نیاز به ارزیابی، grounding و human review | تمرکز GenAI Profile بر ریسک‌های GenAI |
| افشای داده حساس | data، prompt، logging | حریم خصوصی، امنیت | باید data minimization و redaction دیده شود | مدیریت ریسک اطلاعاتی در AI RMF |
| تولید محتوای مضر یا نامناسب | safety layer، UX | safety، compliance | نیاز به guardrail و policy enforcement | رویکرد risk management |
| دشواری accountability | governance، observability | auditability، transparency | تصمیم‌ها، promptها و نسخه‌ها باید قابل ردیابی باشند | چارچوب مدیریت ریسک NIST |
| استفاده‌ی خارج از context مجاز | product boundary، access control | reliability، safety | معماری باید محدودیت کاربرد و misuse handling داشته باشد | تأکید بر context و governance |

## راهکارها و تاکتیک‌های پیشنهادی

| راهکار / تاکتیک | مسئله‌ای که حل می‌کند | محدودیت | امکان استفاده در گزارش |
|---|---|---|---|
| risk assessment پیش از استقرار | شناخت آسیب‌های محتمل | نیازمند مشارکت ذی‌نفعان | بسیار بالا |
| logging و traceability | پاسخ‌گویی و تحلیل incident | ریسک حریم خصوصی در لاگ | بالا |
| human-in-the-loop برای کاربردهای حساس | کاهش ریسک تصمیم خودکار | هزینه و کاهش سرعت | بالا در دامنه‌های حساس |
| policy و guardrail layer | کنترل خروجی و misuse | guardrailها کامل نیستند | بالا |
| red-teaming و evaluation مداوم | کشف ریسک پیش از production | هزینه‌بر و ناقص | بالا |

## معیارها و شاخص‌های ارزیابی

- معیار: incident rate
- کاربرد: سنجش رخدادهای عملیاتی، safety یا privacy
- محدودیت: رخدادهای گزارش‌نشده دیده نمی‌شوند

- معیار: harmful output rate
- کاربرد: ارزیابی guardrail و policy enforcement
- محدودیت: تعریف harm وابسته به context است

- معیار: privacy leakage tests
- کاربرد: سنجش احتمال افشای داده حساس
- محدودیت: همه‌ی مسیرهای leakage قابل تست نیستند

- معیار: audit coverage
- کاربرد: بررسی اینکه چند درصد تصمیم‌ها قابل ردیابی‌اند
- محدودیت: logging زیاد می‌تواند ریسک privacy ایجاد کند

## کیفیت و محدودیت منبع

- نوع شواهد: چارچوب و پروفایل مدیریت ریسک
- قوت اصلی: فراهم‌کردن زبان و ساختار governance برای GenAI
- ضعف اصلی: تاکتیک‌های اجرایی را در سطح معماری نرم‌افزار با جزئیات پیاده‌سازی توضیح نمی‌دهد
- میزان اتکا در گزارش: بسیار بالا برای بخش ریسک، governance و ویژگی‌های کیفی غیرعملکردی

## جایگاه در گزارش نهایی

- بخش ریسک‌های معماری GenAI
- بخش governance و مسئولیت‌پذیری
- بخش ویژگی‌های کیفی مانند safety، privacy، auditability و transparency
- بخش پیشنهادهای کنترلی برای production

## نکته‌های قابل نقل یا استفاده

- GenAI باید با نگاه risk management طراحی و اداره شود، نه فقط با metricهای دقت و latency.
- معماری GenAI باید کنترل‌های ریسک را به componentهای واقعی تبدیل کند.
- context استفاده و آسیب احتمالی، نوع کنترل‌های لازم را تعیین می‌کند.

## جمع‌بندی نهایی برای این منبع

این منبع برای گزارش نقش چارچوب حاکمیتی دارد. منابع فنی نشان می‌دهند سامانه‌های GenAI چگونه ساخته می‌شوند؛ NIST توضیح می‌دهد این سامانه‌ها چگونه باید از منظر ریسک، اعتماد، حریم خصوصی و مسئولیت‌پذیری کنترل شوند.

# Retrieval-Augmented Generation for AI-Generated Content: A Survey

## شناسنامه
- کلید BibTeX: `zhao2024ragAigcSurvey`
- نوع منبع: مقاله‌ی مروری / survey
- سال: 2024
- نویسندگان: Penghao Zhao, Hailin Zhang, Qinhan Yu, Zhengren Wang, Yunteng Geng, Fangcheng Fu, Ling Yang, Wentao Zhang, Jie Jiang, Bin Cui
- محل انتشار / ناشر: arXiv
- وضعیت مطالعه: خلاصه‌شده
- فایل PDF مبنا: `references/pdfs/zhao2024ragAigcSurvey-2402.19473.pdf`

## مسئله‌ی اصلی
این مقاله کاربرد RAG را در زمینه‌ی AIGC بررسی می‌کند. مسئله‌ی اصلی این است که سامانه‌های تولید محتوا با وجود پیشرفت مدل‌های مولد، همچنان با دانش قدیمی، داده‌های long-tail، خطر نشت داده، هزینه‌ی بالای آموزش و inference و ضعف factuality روبه‌رو هستند. RAG با افزودن retrieval به فرایند تولید، تلاش می‌کند این محدودیت‌ها را با حافظه‌ی غیرپارامتری و قابل‌به‌روزرسانی کاهش دهد.

## پیام محوری
پیام محوری مقاله این است که RAG فقط مخصوص پرسش‌وپاسخ متنی نیست؛ یک الگوی معماری عمومی برای اتصال retriever و generator در انواع سناریوهای AIGC است. این الگو می‌تواند در متن، کد، تصویر، ویدئو، صوت، دانش و حتی کاربردهای علمی ظاهر شود، اما در هر modality نیازمند تنظیم retriever، generator و روش augmentation است.

## ارتباط با معماری نرم‌افزار
این منبع برای معماری نرم‌افزار مفید است چون RAG را به‌عنوان یک معماری compositional معرفی می‌کند: retriever، data store، augmentation method و generator. از این دید، کیفیت سامانه فقط تابع مدل زبانی نیست؛ بلکه به کیفیت index، روش retrieval، چگونگی ورود context به generation و ارزیابی end-to-end وابسته است.

## چالش‌های معماری استخراج‌شده
| چالش | لایه‌ی درگیر | ویژگی کیفی اثرپذیر | پیامد معماری | شاهد از منبع |
|---|---|---|---|---|
| دانش قدیمی و long-tail | data store / retrieval | دقت، تازگی، پوشش | نیاز به حافظه‌ی قابل‌به‌روزرسانی و index مناسب | مقدمه‌ی مقاله درباره محدودیت‌های AIGC |
| تنوع modalityها | retriever / generator | تکامل‌پذیری، نگهداشت‌پذیری | معماری باید قابل تعمیم به modalityهای مختلف باشد | survey کاربردهای متن، کد، تصویر، ویدئو و دانش |
| انتخاب روش augmentation | prompt / latent / logits / pipeline | دقت، latency، پیچیدگی | روش اتصال retriever و generator یک تصمیم معماری است | طبقه‌بندی RAG foundations |
| هزینه‌ی training و inference | model / serving | هزینه، کارایی | RAG می‌تواند بخشی از بار را از مدل پارامتری به حافظه‌ی خارجی منتقل کند | بحث هزینه و کاهش اندازه/گام‌های generation |
| نبود benchmark جامع | evaluation | آزمون‌پذیری، اعتمادپذیری | باید RAG با معیارهای retrieval و generation ارزیابی شود | بخش benchmarks و limitations |

## راهکارها و تاکتیک‌های پیشنهادی
| راهکار / تاکتیک | مسئله‌ای که حل می‌کند | محدودیت | امکان استفاده در گزارش |
|---|---|---|---|
| حافظه‌ی غیرپارامتری قابل‌به‌روزرسانی | دانش قدیمی و long-tail | کیفیت و freshness داده مهم است | زیاد؛ بخش RAG architecture |
| انتخاب retriever متناسب با modality | ضعف retrieval عمومی | نیازمند مدل و index جداگانه | زیاد؛ بخش معماری چندوجهی |
| query-based augmentation | اتصال ساده context به generator | محدودیت context و noise | زیاد؛ برای توضیح RAG پایه |
| enhancementهای retrieval و pipeline | کاهش noise و افزایش relevance | پیچیدگی عملیاتی | زیاد؛ بخش tactical patterns |
| benchmarkهای RAG | ارزیابی کیفیت | نبود معیار واحد برای همه modalityها | متوسط تا زیاد |

## معیارها و شاخص‌های ارزیابی
- معیار: retrieval relevance
- کاربرد: سنجش اینکه داده‌ی بازیابی‌شده با نیاز کاربر مرتبط است یا نه
- محدودیت: در modalityهای مختلف تعریف relevance متفاوت می‌شود

- معیار: factuality / faithfulness
- کاربرد: سنجش وفاداری خروجی به شواهد بازیابی‌شده
- محدودیت: نیازمند داوری یا ground truth است

- معیار: cost و latency
- کاربرد: ارزیابی trade-off میان retrieval، context طولانی و generation
- محدودیت: به مدل، index و workload وابسته است

## کیفیت و محدودیت منبع
- نوع شواهد: مروری / طبقه‌بندی ادبیات
- قوت اصلی: ارائه‌ی دید وسیع از RAG فراتر از متن و LLMهای پرسش‌وپاسخ
- ضعف اصلی: به‌دلیل گستردگی، برای جزئیات عملیاتی RAG در production باید با منابع RAGOps، RAGAs و ARES تکمیل شود
- میزان اتکا در گزارش: متوسط تا زیاد

## جایگاه در گزارش نهایی
- بخش معماری RAG و AIGC
- بخش طبقه‌بندی کاربردها و modalityها
- بخش چالش‌های data freshness، long-tail و cost
- بخش evaluation و محدودیت‌های RAG

## نکته‌های قابل نقل یا استفاده
- RAG را می‌توان به‌عنوان حافظه‌ی غیرپارامتری قابل‌به‌روزرسانی برای سامانه‌های مولد دید.
- طراحی RAG فقط انتخاب retriever نیست؛ روش augmentation میان retriever و generator نیز تصمیم معماری است.
- RAG در modalityهای مختلف یک ایده‌ی مشترک دارد، اما پیاده‌سازی آن وابسته به نوع داده و وظیفه است.

## جمع‌بندی نهایی برای این منبع
این مقاله برای چارچوب‌بندی کلی RAG در گزارش مفید است. ارزش اصلی آن در نشان دادن گستره‌ی RAG در AIGC و استخراج لایه‌های معماری شامل data store، retriever، augmentation و generator است. وزن منبع برای بخش‌های taxonomy و معماری RAG متوسط تا زیاد است، اما برای عملیات و ارزیابی production باید با منابع تخصصی‌تر تکمیل شود.
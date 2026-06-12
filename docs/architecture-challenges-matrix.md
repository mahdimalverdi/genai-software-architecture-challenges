# ماتریس چالش‌های معماری سامانه‌های GenAI

## چکیده

این سند خروجی تحلیلی مرحله‌ی خلاصه‌سازی منابع است. هدف آن تبدیل مقاله‌ها و منابع خوانده‌شده به مجموعه‌ای از چالش‌های معماری، ویژگی‌های کیفی اثرپذیر، پیامدهای طراحی و تاکتیک‌های پیشنهادی است. برخلاف فایل‌های `papers/` که هرکدام یک منبع را جداگانه خلاصه می‌کنند، این سند نگاه بین‌منبعی دارد و می‌تواند مستقیماً در گزارش نهایی استفاده شود.

## روش استخراج

برای هر منبع، بخش‌های «چالش‌های معماری استخراج‌شده»، «راهکارها و تاکتیک‌های پیشنهادی»، «معیارها و شاخص‌های ارزیابی» و «جایگاه در گزارش نهایی» بررسی شده‌اند. سپس چالش‌ها در چند خوشه‌ی معماری تجمیع شده‌اند:

- سامانه‌های RAG و زنجیره‌ی بازیابی تا تولید
- ارزیابی، پایش و کنترل کیفیت خروجی
- hallucination و اعتمادپذیری پاسخ
- prompt injection و امنیت لایه‌ی ورودی/ابزار
- serving، inference، latency و هزینه‌ی اجرا
- MLOps/LLMOps و چرخه‌ی عمر عملیاتی
- governance، risk management و کنترل سازمانی

## ماتریس چالش‌های اصلی

| شناسه | چالش معماری | منابع پشتیبان | لایه‌ی درگیر | ویژگی کیفی اثرپذیر | پیامد معماری | تاکتیک یا تصمیم پیشنهادی |
|---|---|---|---|---|---|---|
| C01 | خطای مرحله‌ای در زنجیره‌ی RAG | `barnett2024sevenFailurePointsRag`, `gao2023ragSurvey`, `gupta2024ragComprehensiveSurvey`, `zhao2024ragAigcSurvey` | ingestion، retrieval، ranking، prompt assembly، generation | صحت، قابلیت اطمینان، ردیابی‌پذیری | پاسخ نهایی ممکن است غلط باشد، بدون اینکه مشخص باشد خطا از داده، بازیابی یا مدل آمده است | تفکیک pipeline به مراحل قابل مشاهده، ثبت query/context/retrieved documents، ارزیابی جداگانه‌ی retrieval و generation |
| C02 | کیفیت پایین یا ناکافی بودن context بازیابی‌شده | `es2023ragas`, `yu2024ragEvaluationSurvey`, `gao2023ragSurvey`, `xu2025ragops` | retriever، vector store، reranker | دقت، completeness، testability | مدل با وجود توانایی زبانی بالا، پاسخ ناقص یا بی‌ربط تولید می‌کند | استفاده از context precision/recall، hit@k، reranking، query rewriting و ارزیابی regression برای index |
| C03 | hallucination و پاسخ بدون پشتوانه | `huang2023hallucinationSurvey`, `manakul2023selfcheckgpt`, `es2023ragas`, `liu2023geval` | generation، evaluation، monitoring | trustworthiness، correctness، safety | خروجی قانع‌کننده اما نادرست تولید می‌شود و ممکن است وارد تصمیم کاربر یا سیستم شود | faithfulness/groundedness evaluation، self-consistency checks، citation-aware output، human review برای موارد پرریسک |
| C04 | اتکا به داوری خود مدل برای ارزیابی | `zheng2023llmJudge`, `liu2023geval`, `yu2024ragEvaluationSurvey`, `saadfalcon2023ares` | evaluation pipeline | validity، repeatability، auditability | معیارهای ارزیابی ممکن است ناپایدار، سوگیرانه یا غیرقابل بازتولید باشند | تعریف rubric، استفاده از چند evaluator، نگه‌داری نمونه‌های طلایی، ثبت prompt ارزیاب و نسخه‌ی مدل evaluator |
| C05 | prompt injection مستقیم و غیرمستقیم | `liu2023formalizingPromptInjection`, `greshake2023indirectPromptInjection`, `yi2023bipia`, `liu2023houyi`, `owasp2025llmTop10` | input layer، retrieval layer، tool invocation، agent orchestration | security، integrity، safety | داده‌ی بیرونی یا ورودی کاربر می‌تواند دستور پنهان وارد کند و رفتار مدل یا ابزارها را منحرف کند | جداسازی instruction از data، content sanitization، policy gate پیش از tool call، least privilege برای ابزارها، logging و abuse detection |
| C06 | ریسک استفاده از منابع بیرونی در RAG و agentها | `yi2023bipia`, `greshake2023indirectPromptInjection`, `owasp2025llmTop10`, `zhao2024ragAigcSurvey` | retrieval، connector، browser/tool layer | security، privacy، reliability | محتوای بازیابی‌شده می‌تواند غیرقابل اعتماد یا خصمانه باشد | طبقه‌بندی trust level برای sourceها، sandbox برای ابزارها، allowlist/denylist، provenance tracking |
| C07 | دشواری serving مدل‌های بزرگ در مقیاس بالا | `kwon2023pagedattention`, `zheng2023sglang`, `zhong2024distserve`, `li2024llmInferenceServingSurvey` | inference serving، scheduler، memory manager | performance، scalability، cost efficiency | latency بالا، مصرف حافظه زیاد و throughput پایین باعث ناپایداری تجربه‌ی کاربر و هزینه‌ی عملیاتی می‌شود | batching هوشمند، KV-cache management، disaggregation prefill/decode، autoscaling، queue policy و capacity planning |
| C08 | جدال latency، کیفیت و هزینه | `li2024llmInferenceServingSurvey`, `kwon2023pagedattention`, `zhong2024distserve`, `zhen2025tamingTitans` | model serving، routing، model selection | performance، cost، availability | استفاده از مدل بزرگ برای همه‌ی درخواست‌ها هزینه و زمان پاسخ را بالا می‌برد | model routing، fallback مدل کوچک‌تر، caching، budget-aware generation، timeout و degradation policy |
| C09 | نبود چرخه‌ی عمر عملیاتی برای GenAI | `stone2025navigatingMlops`, `huyen2025aiEngineering`, `engineeringAiSystems2025`, `xu2025ragops` | platform، CI/CD، monitoring، governance | maintainability، operability، reproducibility | کیفیت سیستم پس از release افت می‌کند و تغییر مدل/داده قابل کنترل نیست | LLMOps/RAGOps pipeline، versioning برای prompt/model/index/data، release gates، rollback strategy |
| C10 | drift در داده، رفتار کاربر و corpus | `stone2025navigatingMlops`, `xu2025ragops`, `gao2023ragSurvey`, `huyen2025aiEngineering` | data pipeline، monitoring | reliability، correctness | سیستم بدون تغییر کد به‌تدریج پاسخ‌های ضعیف‌تر می‌دهد | drift monitoring، scheduled re-indexing، freshness policy، data quality checks |
| C11 | نبود observability کافی برای عیب‌یابی پاسخ | `barnett2024sevenFailurePointsRag`, `xu2025ragops`, `engineeringAiSystems2025`, `es2023ragas` | runtime، logging، tracing، evaluation | diagnosability، auditability | تیم نمی‌تواند بفهمد چرا پاسخ اشتباه تولید شده است | trace کامل request، ذخیره‌ی retrieved docs و prompt assembled، correlation ID، dashboard برای quality metrics |
| C12 | ابهام در مالکیت کیفیت | `stone2025navigatingMlops`, `huyen2025aiEngineering`, `engineeringAiSystems2025`, `nist2024genAiProfile` | process، team topology، governance | maintainability، accountability | کیفیت بین تیم مدل، محصول، backend و عملیات پخش می‌شود و مالک مشخص ندارد | تعریف RACI، quality owner، review process، risk register و معماری مبتنی بر مسئولیت مشترک |
| C13 | ریسک‌های حقوقی، اخلاقی و حریم خصوصی | `nist2024genAiProfile`, `owasp2025llmTop10`, `huyen2025aiEngineering`, `minaee2024llmSurvey` | governance، data handling، output policy | compliance، privacy، safety | داده‌ی حساس ممکن است وارد prompt، log یا خروجی شود | data minimization، PII redaction، access control، retention policy، human escalation |
| C14 | وابستگی شدید به prompt و ناپایداری رفتار سیستم | `liu2023geval`, `zheng2023llmJudge`, `huyen2025aiEngineering`, `engineeringAiSystems2025` | prompt layer، evaluation، release process | reproducibility، testability | تغییر کوچک در prompt یا مدل می‌تواند رفتار سیستم را عوض کند | prompt versioning، prompt tests، golden set، canary release و rollback prompt |
| C15 | پیچیدگی معماری در سیستم‌های agentic و tool-using | `owasp2025llmTop10`, `greshake2023indirectPromptInjection`, `huyen2025aiEngineering`, `engineeringAiSystems2025` | agent orchestration، tool layer، authorization | safety، security، reliability | مدل می‌تواند از ابزارها به‌صورت ناخواسته یا مخرب استفاده کند | policy enforcement پیش از action، permission scoping، human-in-the-loop برای actionهای حساس، action audit log |

## نگاشت چالش‌ها به بخش‌های گزارش نهایی

| بخش گزارش | چالش‌های اصلی قابل استفاده | منابع کلیدی |
|---|---|---|
| تعریف مسئله و چرایی معماری GenAI | C09, C10, C12, C14 | `engineeringAiSystems2025`, `huyen2025aiEngineering`, `stone2025navigatingMlops` |
| RAG به‌عنوان مسئله‌ی معماری | C01, C02, C06, C11 | `barnett2024sevenFailurePointsRag`, `gao2023ragSurvey`, `gupta2024ragComprehensiveSurvey`, `zhao2024ragAigcSurvey` |
| ارزیابی و پایش کیفیت | C03, C04, C11, C14 | `es2023ragas`, `liu2023geval`, `zheng2023llmJudge`, `yu2024ragEvaluationSurvey`, `saadfalcon2023ares` |
| امنیت و prompt injection | C05, C06, C13, C15 | `liu2023formalizingPromptInjection`, `greshake2023indirectPromptInjection`, `yi2023bipia`, `owasp2025llmTop10` |
| serving و کارایی | C07, C08 | `kwon2023pagedattention`, `zheng2023sglang`, `zhong2024distserve`, `li2024llmInferenceServingSurvey`, `zhen2025tamingTitans` |
| عملیات، نگه‌داری و governance | C09, C10, C12, C13 | `stone2025navigatingMlops`, `xu2025ragops`, `nist2024genAiProfile`, `huyen2025aiEngineering` |

## تاکتیک‌های معماری قابل دفاع در گزارش

| تاکتیک | چالش‌هایی که پوشش می‌دهد | توضیح کاربردی |
|---|---|---|
| Observability انتهابه‌انتها | C01, C02, C03, C11 | هر پاسخ باید با query، context، model version، prompt version و evaluator result قابل ردیابی باشد. |
| Evaluation pipeline مستقل از runtime | C02, C03, C04, C14 | قبل از release و پس از تغییر مدل/Prompt/Index، مجموعه‌ای از آزمون‌های کیفیت اجرا شود. |
| جداسازی instruction و data | C05, C06, C15 | متن بازیابی‌شده یا ورودی کاربر نباید با دستورهای سیستمی در یک سطح اعتماد قرار گیرد. |
| Versioning چندلایه | C09, C10, C14 | نسخه‌ی مدل، prompt، embedding model، index، corpus و evaluator باید جداگانه ثبت شود. |
| Policy gate پیش از tool invocation | C05, C13, C15 | هر action بیرونی باید از سیاست امنیتی و مجوز عبور کند، نه اینکه مستقیماً از خروجی مدل اجرا شود. |
| Model routing و degradation policy | C07, C08 | براساس نوع درخواست، هزینه، latency و حساسیت، مدل مناسب انتخاب شود و fallback تعریف شود. |
| Human-in-the-loop هدفمند | C03, C04, C13, C15 | برای تصمیم‌های پرریسک، خروجی غیرقطعی یا actionهای حساس از بازبینی انسانی استفاده شود. |
| Risk register و governance process | C12, C13, C15 | ریسک‌های GenAI باید مالک، معیار پایش، سطح شدت و مسیر escalation داشته باشند. |

## جمع‌بندی تحلیلی

منابع نشان می‌دهند که چالش اصلی سامانه‌های GenAI فقط «بهتر کردن مدل» نیست. معماری باید چند زنجیره‌ی هم‌زمان را کنترل کند: زنجیره‌ی داده و بازیابی، زنجیره‌ی prompt و generation، زنجیره‌ی ارزیابی و پایش، زنجیره‌ی امنیت و کنترل action، و زنجیره‌ی serving و هزینه. بنابراین گزارش نهایی باید GenAI را به‌عنوان یک مسئله‌ی معماری چندلایه تحلیل کند، نه صرفاً یک قابلیت مبتنی بر API مدل زبانی.

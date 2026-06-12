# طرح تفصیلی گزارش نهایی

## چکیده

این سند، طرح تفصیلی گزارش نهایی پروژه را مشخص می‌کند. مبنای این طرح، خلاصه‌های موجود در پوشه‌ی `papers/` و ماتریس تحلیلی `docs/architecture-challenges-matrix.md` است. هدف گزارش نهایی این است که نشان دهد سامانه‌های مبتنی بر مدل‌های زبانی بزرگ و بازیابی‌افزوده، صرفاً مسئله‌ی مدل یا پیاده‌سازی نیستند، بلکه مجموعه‌ای از تصمیم‌های معماری درباره‌ی کیفیت، امنیت، ارزیابی، عملیات، هزینه و حاکمیت را تحمیل می‌کنند.

گزارش باید مسئله‌محور نوشته شود: ابتدا نشان دهد چرا معماری سامانه‌های GenAI دشوار است، سپس چالش‌ها را در خوشه‌های اصلی تحلیل کند و در پایان تاکتیک‌های معماری قابل دفاع ارائه دهد.

## پرسش اصلی گزارش

پرسش اصلی گزارش:

> در طراحی سامانه‌های نرم‌افزاری مبتنی بر GenAI، به‌ویژه سامانه‌های RAG و ابزارمحور، چه چالش‌های معماری تکرارشونده‌ای پدیدار می‌شود و چه تاکتیک‌هایی می‌تواند این چالش‌ها را کنترل کند؟

پاسخ گزارش باید بر چهار محور استوار باشد:

1. چالش‌های کیفیت و اعتمادپذیری خروجی؛
2. چالش‌های امنیتی و prompt injection؛
3. چالش‌های عملیاتی، serving و هزینه؛
4. چالش‌های چرخه‌ی عمر، governance و مسئولیت کیفیت.

## ساختار پیشنهادی گزارش

### ۱. مقدمه و صورت مسئله

**پیام فصل:**
سامانه‌های GenAI به‌دلیل ماهیت احتمالاتی مدل، وابستگی به داده‌ی بیرونی، استفاده از prompt، نیاز به ارزیابی پیوسته و امکان اتصال به ابزارها، با سامانه‌های نرم‌افزاری کلاسیک تفاوت معماری دارند.

**محورهای اصلی:**

- تعریف کوتاه GenAI، LLM و RAG؛
- تفاوت میان «استفاده از مدل» و «ساخت سامانه‌ی نرم‌افزاری قابل اتکا با مدل»؛
- توضیح اینکه کیفیت سیستم فقط به مدل وابسته نیست و به pipeline، داده، prompt، ارزیابی، runtime و governance بستگی دارد؛
- بیان مسئله‌ی گزارش: چگونه این وابستگی‌ها به چالش معماری تبدیل می‌شوند؟

**چالش‌های ماتریس قابل استفاده:**
`C09`, `C10`, `C12`, `C14`

**منابع پشتیبان:**
`engineeringAiSystems2025`, `huyen2025aiEngineering`, `stone2025navigatingMlops`, `minaee2024llmSurvey`

**خروجی مورد انتظار فصل:**
خواننده باید بفهمد چرا موضوع گزارش، بررسی الگوریتم یا مدل نیست، بلکه تحلیل معماری سامانه‌های GenAI است.

### ۲. پیش‌زمینه و مفاهیم کلیدی

**پیام فصل:**
برای تحلیل معماری، باید اجزای اصلی سامانه‌ی GenAI و نقش هرکدام در کیفیت نهایی روشن شود.

**محورهای اصلی:**

- مدل زبانی بزرگ و محدودیت‌های آن؛
- مفهوم prompt، context و instruction؛
- معماری RAG: ingestion، embedding، vector store، retriever، reranker، prompt assembly، generator؛
- مفهوم evaluation pipeline و LLM-as-a-judge؛
- مفهوم serving، inference، batching، KV cache و latency؛
- مفهوم MLOps، LLMOps و RAGOps.

**چالش‌های ماتریس قابل استفاده:**
`C01`, `C02`, `C04`, `C07`, `C09`

**منابع پشتیبان:**
`vaswani2017attention`, `lewis2020rag`, `gao2023ragSurvey`, `gupta2024ragComprehensiveSurvey`, `li2024llmInferenceServingSurvey`, `xu2025ragops`

**خروجی مورد انتظار فصل:**
یک زبان مشترک برای فصل‌های بعدی ساخته شود تا تحلیل چالش‌ها پراکنده و اصطلاح‌محور نشود.

### ۳. RAG به‌عنوان مسئله‌ی معماری

**پیام فصل:**
RAG فقط اضافه کردن یک retriever به مدل نیست؛ یک زنجیره‌ی چندمرحله‌ای است که خطا در هر مرحله می‌تواند پاسخ نهایی را خراب کند.

**محورهای اصلی:**

- خطای مرحله‌ای در RAG و دشواری پیدا کردن منشأ خطا؛
- کیفیت context و اثر آن بر پاسخ نهایی؛
- تفاوت خطای retrieval، خطای ranking، خطای prompt assembly و خطای generation؛
- خطر استفاده از منابع بیرونی غیرقابل اعتماد؛
- نیاز به trace و observability برای query، اسناد بازیابی‌شده، prompt نهایی و خروجی مدل.

**چالش‌های ماتریس قابل استفاده:**
`C01`, `C02`, `C06`, `C11`

**منابع پشتیبان:**
`barnett2024sevenFailurePointsRag`, `gao2023ragSurvey`, `gupta2024ragComprehensiveSurvey`, `zhao2024ragAigcSurvey`, `es2023ragas`, `yu2024ragEvaluationSurvey`, `xu2025ragops`

**تاکتیک‌های قابل طرح:**

- تفکیک pipeline به مراحل قابل مشاهده؛
- ثبت query، context، retrieved documents و prompt assembled؛
- ارزیابی جداگانه‌ی retrieval و generation؛
- استفاده از context precision، context recall و faithfulness؛
- versioning برای index، embedding model و corpus.

**خروجی مورد انتظار فصل:**
گزارش باید نشان دهد خطاهای RAG منشأهای مختلف دارند و کنترل آن‌ها نیازمند طراحی معماری، نه صرفاً tuning مدل، است.

### ۴. ارزیابی، پایش و اعتمادپذیری خروجی

**پیام فصل:**
در سامانه‌های GenAI، تست سنتی کافی نیست؛ چون خروجی‌ها احتمالاتی، متنی، وابسته به context و گاهی بدون پاسخ قطعی‌اند. بنابراین evaluation pipeline باید به‌عنوان جزء معماری طراحی شود.

**محورهای اصلی:**

- hallucination و پاسخ بدون پشتوانه؛
- تفاوت correctness، faithfulness، relevance و completeness؛
- LLM-as-a-judge و محدودیت‌های آن؛
- self-checking و روش‌های تشخیص hallucination؛
- ارزیابی offline، regression evaluation و monitoring بعد از release؛
- لزوم golden set و rubric.

**چالش‌های ماتریس قابل استفاده:**
`C03`, `C04`, `C11`, `C14`

**منابع پشتیبان:**
`huang2023hallucinationSurvey`, `manakul2023selfcheckgpt`, `es2023ragas`, `liu2023geval`, `zheng2023llmJudge`, `yu2024ragEvaluationSurvey`, `saadfalcon2023ares`

**تاکتیک‌های قابل طرح:**

- طراحی evaluation pipeline مستقل از runtime؛
- نگه‌داری golden dataset؛
- ثبت نسخه‌ی evaluator، prompt ارزیاب و rubric؛
- استفاده از چند evaluator برای کاهش سوگیری؛
- تعریف آستانه‌های quality gate پیش از release.

**خروجی مورد انتظار فصل:**
خواننده باید ببیند که ارزیابی در GenAI یک فعالیت جانبی نیست، بلکه یک جزء معماری برای کنترل کیفیت و ریسک است.

### ۵. امنیت، prompt injection و مرز اعتماد

**پیام فصل:**
در سامانه‌های GenAI، ورودی فقط داده نیست؛ ممکن است دستور باشد. این مسئله مرز میان data و instruction را مبهم می‌کند و باعث می‌شود امنیت در سطح prompt، retrieval و tool invocation مطرح شود.

**محورهای اصلی:**

- prompt injection مستقیم و غیرمستقیم؛
- حمله از طریق محتوای بازیابی‌شده یا صفحات وب؛
- خطر اتصال مدل به ابزارها و actionهای واقعی؛
- مسئله‌ی اعتماد به منابع بیرونی؛
- ارتباط prompt injection با privacy، data leakage و unauthorized action؛
- نقش OWASP و کنترل‌های امنیتی در معماری.

**چالش‌های ماتریس قابل استفاده:**
`C05`, `C06`, `C13`, `C15`

**منابع پشتیبان:**
`liu2023formalizingPromptInjection`, `greshake2023indirectPromptInjection`, `yi2023bipia`, `liu2023houyi`, `owasp2025llmTop10`, `nist2024genAiProfile`

**تاکتیک‌های قابل طرح:**

- جداسازی instruction از data؛
- sanitization و طبقه‌بندی سطح اعتماد sourceها؛
- policy gate پیش از tool call؛
- least privilege برای ابزارها؛
- human-in-the-loop برای actionهای حساس؛
- audit log برای tool invocation و actionها.

**خروجی مورد انتظار فصل:**
گزارش باید نشان دهد امنیت GenAI فقط فیلتر کردن متن ورودی نیست؛ بلکه نیازمند طراحی مرزهای اعتماد، مجوزدهی ابزار و کنترل مسیرهای داده است.

### ۶. Serving، inference، latency و هزینه

**پیام فصل:**
کیفیت معماری GenAI فقط در پاسخ درست خلاصه نمی‌شود. سامانه باید در مقیاس بالا، با latency قابل قبول و هزینه‌ی قابل کنترل کار کند. serving مدل‌های بزرگ خود یک مسئله‌ی معماری است.

**محورهای اصلی:**

- هزینه‌ی حافظه و محاسبه در inference؛
- latency در prefill و decode؛
- batching، scheduling و throughput؛
- KV cache و مدیریت حافظه؛
- trade-off میان مدل بزرگ، کیفیت، latency و هزینه؛
- routing میان مدل‌ها و fallback.

**چالش‌های ماتریس قابل استفاده:**
`C07`, `C08`

**منابع پشتیبان:**
`kwon2023pagedattention`, `zheng2023sglang`, `zhong2024distserve`, `li2024llmInferenceServingSurvey`, `zhen2025tamingTitans`

**تاکتیک‌های قابل طرح:**

- batching هوشمند؛
- KV-cache management؛
- جداسازی prefill و decode؛
- model routing و fallback به مدل کوچک‌تر؛
- caching پاسخ یا context؛
- capacity planning و budget-aware generation.

**خروجی مورد انتظار فصل:**
خواننده باید بفهمد تصمیم درباره‌ی مدل و runtime، یک تصمیم معماری با اثر مستقیم بر performance، scalability و cost است.

### ۷. عملیات، چرخه‌ی عمر و governance

**پیام فصل:**
سامانه‌ی GenAI بعد از release ثابت نمی‌ماند. مدل، prompt، corpus، رفتار کاربر و معیارهای کیفیت تغییر می‌کنند. بنابراین معماری باید برای تغییر، پایش، rollback و مسئولیت‌پذیری طراحی شود.

**محورهای اصلی:**

- LLMOps و RAGOps؛
- versioning برای model، prompt، index، corpus و evaluator؛
- drift در داده و رفتار کاربر؛
- release gate و rollback؛
- مالکیت کیفیت میان تیم محصول، backend، data، ML و operations؛
- governance و risk management.

**چالش‌های ماتریس قابل استفاده:**
`C09`, `C10`, `C12`, `C13`, `C14`

**منابع پشتیبان:**
`stone2025navigatingMlops`, `xu2025ragops`, `engineeringAiSystems2025`, `huyen2025aiEngineering`, `nist2024genAiProfile`, `sculley2015hiddenDebt`

**تاکتیک‌های قابل طرح:**

- LLMOps/RAGOps pipeline؛
- versioning و traceability؛
- monitoring برای drift و کیفیت؛
- rollback strategy؛
- RACI و تعیین quality owner؛
- risk register و policy برای داده‌های حساس.

**خروجی مورد انتظار فصل:**
گزارش باید نشان دهد بدون چرخه‌ی عمر عملیاتی، حتی سیستم GenAI خوب طراحی‌شده هم به‌مرور دچار افت کیفیت، ریسک امنیتی و بدهی فنی می‌شود.

### ۸. تاکتیک‌ها و الگوهای معماری پیشنهادی

**پیام فصل:**
پس از تحلیل چالش‌ها، باید مجموعه‌ای از تاکتیک‌های معماری قابل دفاع ارائه شود که بتواند در طراحی یا ارزیابی سامانه‌های GenAI استفاده شود.

**تاکتیک‌های اصلی:**

| تاکتیک | چالش‌های پوشش‌داده‌شده | کاربرد در معماری |
|---|---|---|
| Observability انتهابه‌انتها | C01, C02, C03, C11 | ردیابی query، context، prompt، model version و evaluator result |
| Evaluation pipeline مستقل | C02, C03, C04, C14 | کنترل کیفیت قبل و بعد از release |
| مرزبندی اعتماد و policy gate | C05, C06, C13, C15 | کنترل ورودی، منبع بیرونی و tool call |
| Versioning برای prompt/model/index/data | C09, C10, C14 | بازتولیدپذیری و rollback |
| Model routing و degradation policy | C07, C08 | کنترل latency، هزینه و availability |
| Governance و ownership کیفیت | C12, C13 | روشن کردن مسئولیت، ریسک و کنترل سازمانی |

**منابع پشتیبان:**
تمام خوشه‌های منابع، با تمرکز بر `architecture-challenges-matrix.md`.

**خروجی مورد انتظار فصل:**
این فصل باید به گزارش وجه تجویزی بدهد؛ یعنی فقط نگوید مشکل چیست، بلکه نشان دهد معمار نرم‌افزار چه تصمیم‌هایی باید بگیرد.

### ۹. بحث و جمع‌بندی تحلیلی

**پیام فصل:**
چالش‌های GenAI مستقل از هم نیستند. امنیت، ارزیابی، observability، serving و governance به هم وابسته‌اند و معماری باید آن‌ها را به‌صورت یک سیستم واحد ببیند.

**محورهای اصلی:**

- وابستگی میان RAG، hallucination و evaluation؛
- وابستگی میان prompt injection، tool use و governance؛
- trade-off میان کیفیت، latency و هزینه؛
- تفاوت سامانه‌ی demo با سامانه‌ی production؛
- نقش معمار نرم‌افزار در تبدیل قابلیت مدل به سامانه‌ی قابل اتکا.

**خروجی مورد انتظار فصل:**
جمع‌بندی کند که سامانه‌ی GenAI موفق، ترکیبی از model capability، data architecture، security boundary، evaluation pipeline، serving strategy و operational governance است.

### ۱۰. نتیجه‌گیری

**پیام فصل:**
سامانه‌های GenAI به‌دلیل عدم قطعیت خروجی، وابستگی به داده‌ی بیرونی، ریسک‌های امنیتی و هزینه‌ی عملیاتی، نیازمند نگاه معماری جدی هستند. بدون این نگاه، کیفیت سیستم در سطح demo باقی می‌ماند و در production با شکست‌های پنهان مواجه می‌شود.

**نکات پایانی:**

- GenAI یک component نیست؛ یک ecosystem معماری است.
- RAG، evaluation، security و operations باید هم‌زمان طراحی شوند.
- معیارهای کیفیت باید از ابتدا در architecture decisionها دیده شوند.
- تاکتیک‌های معماری باید قابل ردیابی به چالش‌ها و منابع باشند.

## نگاشت فصل‌ها به منابع کلیدی

| فصل | منابع اصلی |
|---|---|
| مقدمه و صورت مسئله | `engineeringAiSystems2025`, `huyen2025aiEngineering`, `stone2025navigatingMlops`, `minaee2024llmSurvey` |
| پیش‌زمینه | `vaswani2017attention`, `lewis2020rag`, `gao2023ragSurvey`, `li2024llmInferenceServingSurvey` |
| RAG | `barnett2024sevenFailurePointsRag`, `gao2023ragSurvey`, `gupta2024ragComprehensiveSurvey`, `zhao2024ragAigcSurvey`, `xu2025ragops` |
| ارزیابی | `es2023ragas`, `liu2023geval`, `zheng2023llmJudge`, `yu2024ragEvaluationSurvey`, `saadfalcon2023ares` |
| امنیت | `liu2023formalizingPromptInjection`, `greshake2023indirectPromptInjection`, `yi2023bipia`, `liu2023houyi`, `owasp2025llmTop10` |
| serving و هزینه | `kwon2023pagedattention`, `zheng2023sglang`, `zhong2024distserve`, `li2024llmInferenceServingSurvey`, `zhen2025tamingTitans` |
| عملیات و governance | `stone2025navigatingMlops`, `xu2025ragops`, `engineeringAiSystems2025`, `huyen2025aiEngineering`, `nist2024genAiProfile`, `sculley2015hiddenDebt` |

## خروجی بعدی پیشنهادی

بعد از این outline، گام بعدی نوشتن نسخه‌ی اولیه‌ی گزارش است. پیشنهاد می‌شود ابتدا سه بخش زیر نوشته شوند:

1. مقدمه و صورت مسئله؛
2. RAG به‌عنوان مسئله‌ی معماری؛
3. ارزیابی و پایش کیفیت.

این سه بخش ستون فقرات گزارش را می‌سازند و بعد از آن می‌توان فصل‌های امنیت، serving و governance را اضافه کرد.

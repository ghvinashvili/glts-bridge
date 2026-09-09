# GLTS Bridge

**G**eorgian **L**anguage **T**oken **S**aver.

`glts` არის ქართული ტრანსლიტერაციის ხიდი [Claude Code](https://claude.com/claude-code)-ისთვის.

მოდელი პასუხს ლათინური სიმბოლოებით წერს, ეკრანზე კი შენ ქართულ დამწერლობას
ხედავ. კოდი, ბრძანებები, ბმულები და ფაილების სახელები უცვლელი რჩება.

```
model:   gamarjoba, Docker daayenda. gaushvi `ddev start`.
ekrani:  გამარჯობა, Docker დააყენდა. გაუშვი `ddev start`.
```

## რატომ

ქართული ასო UTF-8-ში სამ ბაიტს იკავებს და მოდელის ტოკენიზატორი მას რამდენიმე
ტოკენად ჭრის. იგივე ტექსტი ლათინური ასოებით ორჯერ-სამჯერ ნაკლებ ტოკენს ხარჯავს.
`glts` საშუალებას გაძლევს ტოკენები ლათინურად დაზოგო, კითხვა კი ქართულად
განაგრძო.

## როგორ მუშაობს

Claude Code-ს აქვს `MessageDisplay` hook, რომელიც ყოველ ჯერზე ეშვება, როცა
ასისტენტის შეტყობინების ახალი ნაწილი ეკრანზე გამოდის. hook-ს stdin-ზე მოსდის
JSON ველებით `turn_id`, `message_id`, `index`, `final` და `delta`. პასუხად
დაბრუნებული `displayContent` ეკრანზე ჩაანაცვლებს ორიგინალ ტექსტს.

მთავარი დეტალი: ჩანაცვლება მხოლოდ ჩვენებას ეხება. ტრანსკრიპტში და მოდელის
კონტექსტში ტექსტი ლათინურად რჩება. ამიტომ მომდევნო მოთხოვნებში ტოკენების დაზოგვა
ნამდვილად მუშაობს.

`delta` ყოველთვის დასრულებული სტრიქონებია, ბოლო ნაწილის გარდა. ეს საშუალებას
გვაძლევს სტრიქონობრივად ვიმუშაოთ. ღობით შემოსაზღვრული კოდის ბლოკის მდგომარეობა
ნაწილებს შორის დროებით ფაილში ინახება, რომელიც ბოლო ნაწილზე იშლება.

## რა არ შეიძლება

საპირისპირო მიმართულება, ანუ შენი ქართული ტექსტის ლათინურად გადაქცევა მოდელამდე
მისვლისას, ამჟამად შეუძლებელია. `UserPromptSubmit` hook-ს შეუძლია კონტექსტის
დამატება, მაგრამ არა თავად მოთხოვნის ჩანაცვლება. ამიტომ ხიდი ცალმხრივია:
შენ ქართულად წერ, მოდელი ლათინურად პასუხობს, შენ კი ქართულს ხედავ.

სრული გზა ერთი შეკითხვისა:

```
შენ წერ            დააყენე docker
მოდელამდე მიდის    დააყენე docker        <- უცვლელი, ტოკენები არ იზოგება
მოდელი წერს        docker daayenda
შენ ხედავ          docker დააყენდა       <- აქ იზოგება ტოკენები
```

ანუ დაზოგვა მხოლოდ ბოლო ორ ხაზზე ხდება. თუ გინდა, რომ შენი მხარეც გაიაფდეს,
უბრალოდ თვითონ დაწერე ლათინური ასოებით. მოდელი ორივეს ერთნაირად იგებს და
ცხრილთან დამთხვევა არ არის საჭირო.

## ასოების ცხრილი

გარდაქმნა ხარბია და გრძელ თანმიმდევრობას ანიჭებს უპირატესობას. მაგალითად
`ch` ჯერ `ჩ`-ს ეძებს და მხოლოდ შემდეგ იშლება ცალკეულ ასოებად.

| ლათინური | ქართული | ლათინური | ქართული | ლათინური | ქართული |
|---|---|---|---|---|---|
| a | ა | l | ლ | y | ყ |
| b | ბ | m | მ | sh | შ |
| g | გ | n | ნ | ch | ჩ |
| d | დ | o | ო | ts, c | ც |
| e | ე | p | პ | dz | ძ |
| v | ვ | zh | ჟ | w | წ |
| z | ზ | r | რ | tch | ჭ |
| th | თ | s | ს | kh, x | ხ |
| i | ი | t | ტ | j | ჯ |
| k | კ | u | უ | h | ჰ |
| gh | ღ | ph, f | ფ | q | ქ |

## რა რჩება ლათინურად

გარდაქმნა შეგნებულად კონსერვატიულია. უცვლელი რჩება:

- სიტყვა, რომელიც დიდი ასოთი იწყება ან დიდ ასოს შეიცავს, ანუ საკუთარი სახელები
  როგორიცაა `Docker`, `DDEV`, `Drupal`
- ტექსტი უკუტალღებში, როგორც ერთხაზიანი, ისე სამმაგი ღობის ბლოკი
- ბმულები სქემით, მაგალითად `https://` და `ssh://`
- გზები, რომლებიც `/` ან `~/` შეიცავს
- დროშები, რომლებიც `-` ან `--`-ით იწყება
- წერტილიანი სახელები, მაგალითად `settings.json` და `drupal.ddev.site`
- ელფოსტა და `user@host` ფორმის მისამართები
- ციფრები და პუნქტუაცია

ეს ნიშნავს, რომ ქართული ბოლოსართი, რომელიც პირდაპირ გზას ან ბმულს ეწებება,
ლათინურად დარჩება. სჯობს ასეთი სიტყვა ცალკე დაიწეროს.

## ინგლისური სიტყვები

პატარა ასოებით დაწერილი ინგლისური სიტყვა სხვა შემთხვევაში ქართულ სისულელედ
გადაიქცეოდა. სიტყვა `hook` გახდებოდა „ჰოოკ“. ამის თავიდან ასაცილებლად ორი
მექანიზმია.

**ლექსიკონი.** ფაილი `data/keep.txt` შეიცავს სიტყვებს, რომლებიც ყოველთვის
ლათინურად რჩება. თითო სიტყვა ხაზზე, `#` კომენტარია. შენი პირადი სია, თუ არსებობს
მისამართზე `~/.config/glts/keep.txt`, ზემოდან ერთვის, ანუ რეპოზიტორიის
რედაქტირება არ გჭირდება.

**გაქცევის ნიშანი.** ხაზი სიტყვის წინ ერთჯერადად იცავს მას. `\gamarjoba`
დაბრუნდება როგორც gamarjoba, ლათინურად.

### ქართული ბოლოსართი

დეფისის შემდეგ მოსული ნაწილი ყოველთვის ქართულად გარდაიქმნება, თუნდაც სიტყვის
თავი ლათინური დარჩეს. ეს ზუსტად ის წესია, რომელსაც ქართული უცხო სიტყვებთან
იყენებს.

| დაწერილი | ნაჩვენები |
|---|---|
| `python-is` | python-ის |
| `docker-shi` | docker-ში |
| `GitHub-ze` | GitHub-ზე |

იგივე მუშაობს უკუტალღების შემდეგაც, ანუ `` `settings.json`-shi `` გამოჩნდება
როგორც `settings.json`-ში.

### დიგრაფის გახლეჩა

გარდაქმნა ხარბია, ამიტომ სიტყვა `khidze` წაიკითხება როგორც ხიძე და არა ხიდზე.
აპოსტროფი სიტყვის შიგნით ამ წყვილს ხლეჩს და თვითონ ქრება: `khid'ze` გამოჩნდება
როგორც ხიდზე.

### შეჯახებები

ზოგი ინგლისური სიტყვა ლათინურად დაწერილ ქართულ სიტყვასაც ჰგავს. სწორედ ამიტომ
სია მოკლე ინგლისურ სიტყვებს არ შეიცავს. `is`, `am`, `an`, `or`, `as`, `var` და
`ver` ერთდროულად ქართული სიტყვებია: ის, ამ, ან, ორ, ას, ვარ, ვერ. თუ ასეთი
სიტყვა მართლაც ინგლისურად გჭირდება, გამოიყენე გაქცევის ნიშანი.

## ტერმინალის მომზადება

ორი ხარვეზი ტერმინალში ქართულს გამოუსადეგარს ხდის და არც ერთი მათგანი ამ
პროექტს არ ეკუთვნის. ისინი ჯერ უნდა გასწორდეს.

**შრიფტი.** პროგრამისტული შრიფტების უმეტესობას ქართული ასოები არ აქვს, ამიტომ
ტერმინალი პროპორციულ ქართულ შრიფტს ეშვება. ფიქსირებულ უჯრედებში ასეთი ასოები
ერთმანეთზე ეხვევა და ტექსტი მიჭყლეტილი ჩანს. გამოსავალი არის `DejaVu Sans Mono`,
ნამდვილი მონოსიგანის შრიფტი სრული ქართული დაფარვით.

**კლავიატურა.** Debian-ის `/etc/inputrc` ტოვებს ჩართულს `convert-meta`
პარამეტრს, რომელიც UTF-8 სიმბოლოს მაღალ ბაიტებს ESC მიმდევრობებად აქცევს.
ამიტომ ბრძანების სტრიქონში აკრეფილი ქართული ირღვევა, თუმცა იმავე ტექსტის ჩასმა
სწორად მუშაობს.

ორივეს ერთი ბრძანება ასწორებს:

```bash
./setup/setup-terminal.sh
```

მთელი სისტემისთვის, ყველა მომხმარებელზე:

```bash
./setup/setup-terminal.sh --system
```

შემოწმება:

```bash
fc-match 'Monospace:lang=ka'
```

პასუხი `DejaVu Sans Mono` უნდა იყოს. ცვლილება ახალ ტერმინალში ამოქმედდება.

## დაყენება

```bash
git clone https://github.com/ghvinashvili/glts-bridge.git
cd glts-bridge
./install.sh
```

სკრიპტი hook-ს არეგისტრირებს ფაილში `~/.claude/settings.json`, წინა ვერსიის ასლს
ინახავს გვერდით სახელით `settings.json.glts-backup`, და `glts` ბრძანებას დებს
საქაღალდეში `~/.local/bin`. Claude Code კონფიგურაციას ცოცხლად კითხულობს, ანუ
ხიდი ჩვეულებრივ მაშინვე ამოქმედდება. თუ არა, თავიდან გაუშვი.

სრული მოხსნა:

```bash
./uninstall.sh
```

## ბრძანებები

| ბრძანება | რას აკეთებს |
|---|---|
| `glts status` | აჩვენებს, ჩართულია თუ არა ხიდი და სად წერია ჟურნალი |
| `glts watch` | ცოცხლად აჩვენებს ყოველ გარდაქმნას, სანამ Ctrl+C არ დააჭერ |
| `glts try TEXT` | ერთ სტრიქონს გარდაქმნის, არაფერს ცვლის |
| `glts latin FILE` | ქართულ ფაილს ლათინურად ბეჭდავს |
| `glts kartuli FILE` | ლათინურ ფაილს ქართულად ბეჭდავს |
| `glts on` | რთავს ხიდს |
| `glts off` | თიშავს ხიდს |

### ქართული დოკუმენტის წაკითხვა

`glts latin` ქართულ ფაილს ლათინურად ბეჭდავს. ეს იმისთვისაა, რომ მოდელმა
დოკუმენტი გაცილებით ნაკლები ტოკენით წაიკითხოს.

```bash
glts latin სტატია.md
```

კოდის ბლოკები, უკუტალღები, ბმულები და გზები ხელუხლებელი რჩება, ზუსტად ისე
როგორც საპირისპირო მიმართულებაში.

დროშა `--exact` დამატებით ნიშნებს ურთავს, რომ ტექსტი ზუსტად დაუბრუნდეს ქართულს.
ასეთი გამონატანი ოდნავ გრძელია, სამაგიეროდ სრულად შექცევადია. ასი კილობაიტიანი
დოკუმენტი შემოწმებულია და სიმბოლომდე ბრუნდება.

```bash
glts latin --exact სტატია.md
```

### ქართული დოკუმენტის დაწერა

საპირისპირო ბრძანება `glts kartuli` ლათინურ ტექსტს ქართულად აქცევს. ასე
დოკუმენტის დაწერაც იაფდება: მოდელი ლათინურად წერს, ფაილში კი ნამდვილი ქართული
ჯდება.

```bash
glts kartuli chernaxati.txt > statia.md
```

მოქმედებს იგივე წესები: კოდის ბლოკები, უკუტალღები, ბმულები და გზები უცვლელი
რჩება, ლექსიკონის სიტყვები ლათინურად, დეფისის შემდეგ კი ქართული ბოლოსართი.

### თვალყურის დევნება

`glts watch` აჩვენებს ორივე მხარეს: რას აგზავნის მოდელი და რას ხედავ შენ.

```
22:11:49 final
  <- glts mushaobs.
  -> ხიდი მუშაობს.
```

ის შეიძლება მუდმივად გაშვებული გქონდეს მეორე ტერმინალში. სანამ მუშაობს, hook
ყოველ გარდაქმნას წერს ფაილში `~/.local/state/glts/trace.jsonl`. გაჩერებისას
ჩაწერა ავტომატურად ითიშება, რომ ჟურნალი უსასრულოდ არ გაიზარდოს. თუ გინდა, რომ
ჩაწერა გაჩერების შემდეგაც გაგრძელდეს, გამოიყენე `glts watch --keep`. ჟურნალი
ხუთ მეგაბაიტს რომ გადააჭარბებს, თავიდან იწყება.

როცა ჩაწერა გამორთულია, hook მხოლოდ ერთ შემოწმებას აკეთებს და არაფერს წერს
დისკზე. ანუ მუდმივად ჩართული ხიდი დამატებით არაფერს ხარჯავს.

### ჩართვა და გამორთვა

`glts off` hook-ს შლის კონფიგურაციიდან და ჩაწერასაც თიშავს. `glts on` უკან
აბრუნებს. ცვლილება ჩვეულებრივ მაშინვე მოქმედებს.

## ტესტები

```bash
python3 tests/test_glts.py
```

ტესტები ამოწმებს ასოების ცხრილს, დიგრაფების უპირატესობას, კოდისა და ბმულების
ხელშეუხებლობას და ღობით შემოსაზღვრული ბლოკის მდგომარეობას ნაწილებს შორის.

## მოთხოვნები

- Claude Code 2.1.266 ან უფრო ახალი, სადაც `MessageDisplay` hook არსებობს
- Python 3.8 ან უფრო ახალი, გარე ბიბლიოთეკების გარეშე

---

## English

`glts`, the Georgian Language Token Saver, lets Claude Code answer in Latin transliteration while
you read Georgian script. It registers a `MessageDisplay` hook that rewrites the
displayed text only; the stored transcript and the model's own context keep the
Latin form, so the token saving is real across turns.

Code spans, fenced blocks, URLs, paths, command flags, dotted identifiers and
capitalised proper nouns are left exactly as written. The reverse direction is
not possible today: `UserPromptSubmit` can add context but cannot replace the
prompt, so your own Georgian input reaches the model unchanged. One question end
to end:

```
you type          დააყენე docker
model receives    დააყენე docker        <- unchanged, no saving here
model writes      docker daayenda
you see           docker დააყენდა       <- the saving happens here
```

Type in Latin yourself if you want your own side to be cheap too; the model
reads either form, and your spelling need not match the table.

English words are protected two ways: `data/keep.txt` (merged with a personal
`~/.config/glts/keep.txt`) lists words that always stay Latin, and a leading
backslash escapes a single word. A Georgian ending after a hyphen is still
converted, so `python-is` displays as python-ის. Short English function words
are kept off the list on purpose, because `is`, `an`, `or`, `as` and `var` are
also ordinary Georgian words once written in Latin letters.

Before any of this, `./setup/setup-terminal.sh` fixes two things a terminal
gets wrong with Georgian: monospace fonts without Georgian glyphs, which make
the letters collide in the cell grid, and readline's `convert-meta`, which
mangles Georgian typed at the bare prompt. Add `--system` to fix them for
every user.

Install with `./install.sh`, remove with `./uninstall.sh`, test with
`python3 tests/test_glts.py`.

The `glts` CLI controls and inspects the bridge: `glts status` reports whether
it is registered, `glts watch` follows every conversion live in a second
terminal and shows both the Latin that was sent and the Georgian that was
displayed, `glts try TEXT` converts a single line, `glts latin FILE` prints a Georgian
file in Latin so the model can read it for fewer tokens, `glts kartuli FILE`
turns Latin back into Georgian so a document can be written cheaply too, and
`glts on` / `glts off`
switch the bridge itself. Tracing is only written while `watch` is running, so
leaving the bridge on costs nothing.

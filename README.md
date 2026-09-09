# khidi — ხიდი

`khidi` არის ქართული ტრანსლიტერაციის ხიდი [Claude Code](https://claude.com/claude-code)-ისთვის.

მოდელი პასუხს ლათინური სიმბოლოებით წერს, ეკრანზე კი შენ ქართულ დამწერლობას
ხედავ. კოდი, ბრძანებები, ბმულები და ფაილების სახელები უცვლელი რჩება.

```
model:   gamarjoba, Docker daayenda. gaushvi `ddev start`.
ekrani:  გამარჯობა, Docker დააყენდა. გაუშვი `ddev start`.
```

## რატომ

ქართული ასო UTF-8-ში სამ ბაიტს იკავებს და მოდელის ტოკენიზატორი მას რამდენიმე
ტოკენად ჭრის. იგივე ტექსტი ლათინური ასოებით ორჯერ-სამჯერ ნაკლებ ტოკენს ხარჯავს.
`khidi` საშუალებას გაძლევს ტოკენები ლათინურად დაზოგო, კითხვა კი ქართულად
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

## დაყენება

```bash
git clone https://github.com/USER/khidi.git
cd khidi
./install.sh
```

სკრიპტი hook-ს არეგისტრირებს ფაილში `~/.claude/settings.json`, წინა ვერსიის ასლს
ინახავს გვერდით სახელით `settings.json.khidi-backup`, და `khidi` ბრძანებას დებს
საქაღალდეში `~/.local/bin`. ამოქმედებისთვის Claude Code-ის თავიდან გაშვებაა
საჭირო.

სრული მოხსნა:

```bash
./uninstall.sh
```

## ბრძანებები

| ბრძანება | რას აკეთებს |
|---|---|
| `khidi status` | აჩვენებს, ჩართულია თუ არა ხიდი და სად წერია ჟურნალი |
| `khidi watch` | ცოცხლად აჩვენებს ყოველ გარდაქმნას, სანამ Ctrl+C არ დააჭერ |
| `khidi try TEXT` | ერთ სტრიქონს გარდაქმნის, არაფერს ცვლის |
| `khidi on` | რთავს ხიდს |
| `khidi off` | თიშავს ხიდს |

### თვალყურის დევნება

`khidi watch` აჩვენებს ორივე მხარეს: რას აგზავნის მოდელი და რას ხედავ შენ.

```
22:11:49 final
  <- khidi mushaobs.
  -> ხიდი მუშაობს.
```

ის შეიძლება მუდმივად გაშვებული გქონდეს მეორე ტერმინალში. სანამ მუშაობს, hook
ყოველ გარდაქმნას წერს ფაილში `~/.local/state/khidi/trace.jsonl`. გაჩერებისას
ჩაწერა ავტომატურად ითიშება, რომ ჟურნალი უსასრულოდ არ გაიზარდოს. თუ გინდა, რომ
ჩაწერა გაჩერების შემდეგაც გაგრძელდეს, გამოიყენე `khidi watch --keep`. ჟურნალი
ხუთ მეგაბაიტს რომ გადააჭარბებს, თავიდან იწყება.

როცა ჩაწერა გამორთულია, hook მხოლოდ ერთ შემოწმებას აკეთებს და არაფერს წერს
დისკზე. ანუ მუდმივად ჩართული ხიდი დამატებით არაფერს ხარჯავს.

### ჩართვა და გამორთვა

`khidi off` hook-ს შლის კონფიგურაციიდან და ჩაწერასაც თიშავს. `khidi on` უკან
აბრუნებს. ორივე შემთხვევაში Claude Code თავიდან უნდა გაუშვა.

## ტესტები

```bash
python3 tests/test_khidi.py
```

ტესტები ამოწმებს ასოების ცხრილს, დიგრაფების უპირატესობას, კოდისა და ბმულების
ხელშეუხებლობას და ღობით შემოსაზღვრული ბლოკის მდგომარეობას ნაწილებს შორის.

## მოთხოვნები

- Claude Code 2.1.266 ან უფრო ახალი, სადაც `MessageDisplay` hook არსებობს
- Python 3.8 ან უფრო ახალი, გარე ბიბლიოთეკების გარეშე

---

## English

`khidi` (ხიდი, "bridge") lets Claude Code answer in Latin transliteration while
you read Georgian script. It registers a `MessageDisplay` hook that rewrites the
displayed text only; the stored transcript and the model's own context keep the
Latin form, so the token saving is real across turns.

Code spans, fenced blocks, URLs, paths, command flags, dotted identifiers and
capitalised proper nouns are left exactly as written. The reverse direction is
not possible today: `UserPromptSubmit` can add context but cannot replace the
prompt, so your own Georgian input reaches the model unchanged.

Install with `./install.sh`, remove with `./uninstall.sh`, test with
`python3 tests/test_khidi.py`.

The `khidi` CLI controls and inspects the bridge: `khidi status` reports whether
it is registered, `khidi watch` follows every conversion live in a second
terminal and shows both the Latin that was sent and the Georgian that was
displayed, `khidi try TEXT` converts a single line, and `khidi on` / `khidi off`
switch the bridge itself. Tracing is only written while `watch` is running, so
leaving the bridge on costs nothing.

## design notes

# wav - split on silence and store metadata in a sqlite3 db

```
new commandline interface

wavdb
    --db 
    --create
    --update
    --import
    --export
    

    create --from-dir
    split <target> --output --silence-threshold --silence-duration --fade-time --skip-db
    clone <path> <dst> <sql>
    delete <path> <sql> --noconfirm
    shuffle <path> <dst> <sql>
    fx <path> <dst> <sql> <chain>




wavdb <db> (required)
    create (will scan contents)
    select|sql (arbitrary sql)
    update|delete in-place operations
    import <from_path> --format --fx-chain
    export <to_path> --format --sql --fx-chain

OR

wavdb --db (optional path to db with default: $HOME/.wavdb)
    info <path>
    create (will scan contents)
    select|sql (arbitrary sql)
    update|delete in-place operations
    import <from_path> --format --fx-chain
    export <to_path> --format --sql --fx-chain



current commandline interface

wavdb: a sample management app

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --db DB               wav db path (default: None)

subcommands:
  valid subcommands
                        additional help
    cli                 database commandline interface
    clone               clone sample collection
    delete              delete clips in-place
    export              export content from collection
    fx                  apply an fx chain
    info                display analysis
    report              html report from sql query of db
    shuffle             random shuffle of clips
    split               split .wav files on silence thresholds
    test                testing args


wav
    info <path>
    db <collection>
    split <target> --output --silence-threshold --silence-duration --fade-time --skip-db
    clone <path> <dst> <sql>
    delete <path> <sql> --noconfirm
    shuffle <path> <dst> <sql>
    fx <path> <dst> <sql> <chain>


sqlite3 tests-clips/_meta/clips.db \
    -cmd ".mode html" \
    -cmd ".headers on" \
    "select parent, name, channels, bitrate, sample_rate, duration from clips order by duration desc"\
    > report.html
```



## Extensions

Add delete all .wav files with a size between 1M and 3M
```
find . -type f -name '*.wav' -size +1M  -size -3M -delete -print
```



#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""
# wav - split on silence and store metadata in sqlite3 db


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

"""

import argparse
import logging
import os
import random
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import sox

# ------------------------------------------------------------------------------
# Global config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                    datefmt='%H:%M:%S')


# ------------------------------------------------------------------------------
# Templates

report_tmpl = """
<!DOCTYPE html>
<html>
<head>
<style>
table, th, td {{
    border: 0.5px solid grey;
    border-collapse: collapse;
    padding: 10px;
}}
</style>
</head>
<body>
<h1>{title}</h1>
<pre>
{query}
</pre>
<table>
{tbody}
</table>
</body>
</html>"""

VIEWS = [
    ("overview",
        "select parent, name, channels, bitrate, sample_rate, duration from clips order by duration desc"),
]


# ------------------------------------------------------------------------------
# Utility functions and classes


# ------------------------------------------------------------------------------
# Abstract Classes



# ------------------------------------------------------------------------------
# Core App




class SampleInfo:
    FIELDS = [
        ('file',            'text', "file path"),
        ('parent',          'text', "parent folder"),
        ('name',            'text', "file name"),
        ('suffix',          'text', "file suffix e.g .wav"),
        ('encoding',        'text', "file encoding"),
        ('file_size',       'text', "size of file in text format"),
        ('file_size_k',      'integer', "size of file in kilobytes"),

        ('channels',        'integer', "number of channels"),
        ('sample_rate',     'real', "number of samples per second"),
        ('bitdepth',        'integer', "the number of bits of information in each sample"),
        ('bitrate',         'real', "the number of bits that are conveyed or processed per unit of time"),
        ('samples',         'integer', "number of samples"),
        ('duration',        'real', "length of file in seconds"),

        ('mean_norm',       'real', "Arithmetic mean of samples' absolute values"),
        ('max_amp',         'real', "Maximum sample value"),
        ('min_amp',         'real', "Minimum sample value"),
        ('mid_amp',         'real', "Aka mid-range, midpoint between the max and minimum values."),
        ('mean_amp',        'real', "Arithmetic mean of samples' values (also dc_offset)"),
        ('rms_amp',         'real', "Root mean square, root of squared values' mean"),

        ('max_delta',       'real', "Maximum difference between two successive samples"),
        ('min_delta',       'real', "Minimum difference between two successive samples"),
        ('rms_delta',       'real', "Root mean square of differences between successive samples"),
        ('mean_delta',      'real', "Arithmetic mean of differences between successive samples"),

        ('freq',            'integer', "Estimation of the input file's frequency"),
        ('vol_adj',         'real', "Value that should be sent to -v so peak absolute amplitude is 1"),
        ('dc_offset',       'real', "DC shift caused perhaps by a hardware problem in the recording chain"),
        ('crest_factor',    'real', "Standard ratio of peak to RMS level (note: not in dB)"),
        ('flat_factor',     'real', "A measure of the flatness (i.e. consecutive samples with the same value) of the signal at its peak levels"),
        ('scale_max',       'real', "The maximum value that could apply to Max level"),
        ('window_s',        'real', "The length of the window used for the peak and trough RMS measurements"),

        ('peak_level_db',   'real', "Standard peak measured in dBFS"),
        ('rms_level_db',    'real', "Standard RMS level measured in dBFS"),
        ('rms_peak_db',     'real', "Peak values for RMS level measured over a short window (default 50ms)"),
        ('rms_trough_db',   'real', "Trough values for RMS level measured over a short window (default 50ms)"),
        ('peak_count',      'real', "The number of occasions (not the number of samples) that the signal attained either Min level, or Max level"),
    ]
    def __init__(self, path):
        self.path = path

    def rename(self, dikt, old_key, new_key):
        dikt[new_key] = dikt[old_key]
        del dikt[old_key]
        return dikt

    def get_info(self):
        a = self.soxi_info(self.path)
        b = self.stat_info(self.path)
        c = self.stats_info(self.path)

        d = {}
        n_keys = 0
        for i in [a,b,c]:
            n_keys += len(i.keys())
            d.update(i)

        assert len(d.keys()) == n_keys,  f"{n_keys} != {len(d.keys())}"
        return d

    def get_row(self):
        info = self.get_info()
        row = [info[f] for f, _, _ in self.FIELDS]
        return tuple(row)

    def get_output(self, args, **kwargs):
        return subprocess.check_output(args, **kwargs).decode('utf-8')

    def soxi_raw(self, target):
        raw = self.get_output(['soxi', target])
        raw = raw.replace(': ', '| ')

        lines = [x for x in raw.splitlines() if x]

        res = []
        for line in lines:
            a, b = line.split('|')
            a = a.strip().lower().replace(' ', '_')
            b = b.strip().replace("'", "")
            res.append((a, b))
        return dict(res)

    def soxi_info(self, target):
        d = self.soxi_raw(target)
        del d['precision']
        del d['duration']
        rename = self.rename
        d = rename(d, 'input_file', 'file')
        d = rename(d, 'bit_rate', 'bitrate')
        d = rename(d, 'sample_encoding', 'encoding')
        f = Path(d['file'])
        d['file'] = str(Path(f.parent.name) / f.name)
        d['file_size_k'] = self._text_to_kb(d['file_size'])
        d['parent'] = f.parent.stem
        d['name'] = f.stem
        d['suffix'] = f.suffix
        d['encoding'] = ' '.join(d['encoding'].split()[1:])
        # duration_ms = info['duration'] * 1000
        # bpm = int(60_000 / duration_ms) # 60_000 ms in 1 min
        # one_beat = 500 # ms  (120bpm 4:4 time signature)
        # num_beats = duration_ms / one_beat # (120bpm 4:4 time signature)
        # num_bars = num_beats / 4 # (120bpm 4:4 time signature)
        return d

    def _text_to_kb(self, entry):
        val = None
        if entry.endswith('b'):
            val = int(float(entry[:-1]) / 1024)
        elif entry.endswith('M'):
            val = int(float(entry[:-1]) * 1024)
        elif entry.endswith('k'):
            val = int(float(entry[:-1]))
        else:
            raise NotImplementedError
        return val

    def stat_raw(self, target):
        raw = self.get_output(['sox', target, '-n', 'stat'],
            stderr=subprocess.STDOUT)

        lines = [x for x in raw.splitlines() if x]
        res = []
        for line in lines:
            a, b = line.split(':')
            a = a.replace('(', '').replace(')','')
            a = '_'.join(a.strip().lower().split())
            b = float(b.strip())
            res.append((a, b))
        d = dict(res)
        d['samples_read'] = int(d['samples_read'])
        d['rough_frequency'] = int(d['rough_frequency'])
        return d

    def stat_info(self, target):
        d = self.stat_raw(target)
        del d['scaled_by']
        rename = self.rename
        d = rename(d, 'samples_read', 'samples')
        d = rename(d, 'length_seconds', 'duration')
        # d = rename(d, 'mean_norm', 'mean_norm')
        d = rename(d, 'maximum_amplitude', 'max_amp')
        d = rename(d, 'minimum_amplitude', 'min_amp')
        d = rename(d, 'midline_amplitude', 'mid_amp')
        d = rename(d, 'mean_amplitude', 'mean_amp')
        d = rename(d, 'rms_amplitude', 'rms_amp')
        d = rename(d, 'maximum_delta', 'max_delta')
        d = rename(d, 'minimum_delta', 'min_delta')
        # d = rename(d, 'rms_delta', 'rms_delta')
        # d = rename(d, 'mean_delta', 'mean_delta')
        d = rename(d, 'rough_frequency', 'freq')
        d = rename(d, 'volume_adjustment', 'vol_adj')
        return d

    def stats_raw(self, target):
        raw = self.get_output(['sox', target, '-n', 'stats'],
            stderr=subprocess.STDOUT)

        lines = [x for x in raw.splitlines() if x]
        d = {}
        for line in lines:
            frag = line.split()
            val = frag[-1]
            key = '_'.join(frag[:-1]).lower()
            if key == 'bit-depth':
                val = int(val.split('/')[1])
            elif key == 'num_samples':
                val = val
            elif key == 'pk_count':
                val = int(val)
            else:
                val = float(val)
            d[key] = val
        return d

    def stats_info(self, target):
        d = self.stats_raw(target)
        del d['num_samples']
        del d['length_s']
        del d['min_level']
        del d['max_level']
        rename = self.rename
        d = rename(d, 'bit-depth',  'bitdepth')
        d = rename(d, 'pk_lev_db',  'peak_level_db')
        d = rename(d, 'rms_lev_db', 'rms_level_db')
        d = rename(d, 'rms_pk_db',  'rms_peak_db')
        d = rename(d, 'rms_tr_db',  'rms_trough_db')
        d = rename(d, 'pk_count',   'peak_count')
        return d



class SampleCollectionDB:
    def __init__(self, path):
        self.path = Path(path)
        self.db = self.path / '_meta' / 'clips.db'
        self.con = None
        self.cursor = None

    def open(self):
        self.con = sqlite3.connect(str(self.db))
        # self.cursor = self.con.cursor()

    def close(self):
        self.con.close()

    def create(self):
        self.db.parent.mkdir()
        # print(stmt)
        self.open()
        with self.con as con:
            stmt = "CREATE TABLE clips ({0})".format(
                ", ".join(f'{f} {t}' for f,t,_ in SampleInfo.FIELDS))
            con.execute(stmt)
        self.close()

    def populate(self):
        data = []
        for (dirpath, dirnames, filenames) in os.walk(self.path):
            if '_meta' in dirpath:
                continue
            for f in filenames:
                p = Path(os.path.join(dirpath, f))
                row = SampleInfo(str(p)).get_row()
                data.append(row)
        slots = ",".join(len(row) * ['?'])
        self.open()
        with self.con as con:
            con.executemany(f'INSERT INTO clips VALUES ({slots})', data)
        self.close()


class SampleCollection:
    """Manages the lifecycle and features of a sample collection object
    """
    MIN_FILE_SIZE = 1000

    def __init__(self, path, from_dir=None, **config):
        self.path = Path(path)
        self.from_dir = Path(from_dir) if from_dir else None
        self.config = config
        self.name = self.path.stem
        self.db = SampleCollectionDB(path)
        self.log = logging.getLogger(self.__class__.__name__)

    def exists(self):
        return self.path.exists()

    def cmd(self, shell, *args, **kwds):
        os.system(shell.format(*args, **kwds))

    def sox(self, args):
        defaults = ['sox']
        args = defaults + args
        return subprocess.run(args, check=True, capture_output=True)

    def _progressbar(self, it, prefix="", size=60, file=sys.stdout):
        """
        from: https://stackoverflow.com/questions/3160699/python-progress-bar
        """
        count = len(it)
        def show(j):
            x = int(size*j/count)
            file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
            file.flush()
        show(0)
        for i, item in enumerate(it):
            yield item
            show(i+1)
        file.write("\n")
        file.flush()

    def split(self, target=None, no_prefix=False):
        self.log.info("splitting files")
        if not target and self.from_dir:
            target = self.from_dir
        if not self.exists():
            self.path.mkdir()
        else:
            raise Exception(f"Collection already exists {self.path}")

        if target.is_file():
            self.split_file(target, no_prefix)
        else:
            assert target.is_dir(), "Target must be a directory"
            # targets var has to be list for progressbar
            targets = list(target.glob('*.wav'))
            for t in self._progressbar(targets, prefix=" processing: ", size=40):
                self.split_file(t.absolute(), no_prefix)

        if not self.config['skip_db']:
            self.db.create()
            self.db.populate()

    def split_file(self, target, no_prefix=False):
        # self.log.info(f"splitting {target}")
        silence_duration = self.config.get('silence_duration')
        silence_threshold = self.config.get('silence_threshold')
        fade_time = self.config.get('fade_time')

        _prepfile = Path(f'/tmp/norm_{target.name}')
        norm = ['norm']
        self.sox([target, _prepfile] + norm)
        assert _prepfile.exists()

        clips = self.path / Path(target.stem)
        if clips.exists():
            shutil.rmtree(clips)
        clips.mkdir()

        silence = f"silence 1 {silence_duration} {silence_threshold} 1 {silence_duration} {silence_threshold}".split()
        speed = "speed 0.5".split()
        newfile_restart = ": newfile : restart".split()
        if no_prefix:
            body = [_prepfile, f'{clips}/.wav']
        else:
            body = [_prepfile, f'{clips}/{target.stem}-.wav']
        self.sox(body + silence + speed + newfile_restart)

        for f in Path('.').glob(f'{clips}/{target.stem}-*.wav'):
            faded = f'{clips}/{f.stem}-faded.wav'
            fade = f"fade {fade_time} 0".split()
            try:
                self.sox([f, faded] + fade)
                self.cmd(f"mv {faded} {f}")
            except subprocess.CalledProcessError:
                if os.path.getsize(f) < self.MIN_FILE_SIZE:
                    os.remove(f)
                else:
                    print(f"ignored: {f}")
        os.remove(_prepfile)


    def shuffle(self, to, sql):
        """Shuffle collection to destination."""
        raise NotImplementedError

    def apply_fx(self, to, sql=None, chain=None):
        """Apply fx, results to destination"""
        raise NotImplementedError

    def clone(self, to, sql=None):
        """Clone collection to destination."""
        raise NotImplementedError

    def delete(self, sql):
        """Delete members of Collection."""
        raise NotImplementedError


# ------------------------------------------------------------------------------
# Generic utility functions and classes for commandline ops


# option decorator
def option(*args, **kwds):
    def _decorator(func):
        _option = (args, kwds)
        if hasattr(func, 'options'):
            func.options.append(_option)
        else:
            func.options = [_option]
        return func
    return _decorator

# arg decorator
arg = option

# combines option decorators
def option_group(*options):
    def _decorator(func):
        for option in options:
            func = option(func)
        return func
    return _decorator


class MetaCommander(type):
    def __new__(cls, classname, bases, classdict):
        subcmds = {}
        for name, func in list(classdict.items()):
            if name.startswith('do_'):
                name = name[3:]
                subcmd = {
                    'name': name,
                    'func': func,
                    'options': [],
                }
                if hasattr(func, 'options'):
                    subcmd['options'] = func.options
                subcmds[name] = subcmd
        classdict['_argparse_subcmds'] = subcmds
        return type.__new__(cls, classname, bases, classdict)



# ------------------------------------------------------------------------------
# Commandline interface




class Application(metaclass=MetaCommander):
    """wavdb: a sample management app
    """
    name = 'wavdb'
    epilog = ''
    version = '0.1'
    default_args = ['--help']

    def get_config(self, args, exclude_list=None):
        config = vars(args).copy()
        if exclude_list:
            for key in exclude_list:
                del config[key]
        return config


    @arg("path", help="path to audio file")
    def do_info(self, args):
        "display analysis"
        if not os.path.isfile(args.path):
            print("ERROR: path must be a file")
            return
        d = SampleInfo(args.path).get_info()
        for f, t, _ in SampleInfo.FIELDS:
            print(f"{f:<15}\t{t:<15}\t{d[f]:<15}")

    @arg("sql", help="sql query")
    @arg("collection", help="sample collection path")
    @option("-o", "--output", help="output path", default="report.html")
    def do_report(self, args):
        "html report from sql query of db"
        db = Path(args.collection) / '_meta' / 'clips.db'
        # cmd = ['sqlite3', str(db), '-cmd', ".mode html", '-cmd', ".headers on", f"{args.sql}"]
        cmd = ['sqlite3', str(db), '-cmd', ".mode html", '-cmd', ".headers on", args.sql]
        result = subprocess.run(cmd, capture_output=True).stdout.decode('utf-8')
        with open(args.output, 'w') as f:
            report = report_tmpl.format(title="report", query=args.sql, tbody=result)
            f.write(report)

    @arg("collection", help="sample collection path")
    def do_cli(self, args):
        "database commandline interface"
        db = Path(args.collection) / '_meta' / 'clips.db'
        os.system(f'litecli {db}')
        # os.system(f'sqlite3 {db}')


    @arg("target", help=".wav file or folder of .wav files to split")
    @option("-o", "--output", help="output path to new sample collection folder")
    @option("-t", "--silence-threshold", help="split on silence threshold as percent of volume", default="1%")
    @option("-d", "--silence-duration", type=float, help="split on silence duration in seconds", default=0.1)
    @option("-p", "--no-prefix", default=False, action="store_true", help="no prefix from name of each split part")
    @option("-f", "--fade-time", type=float, help="fade time in seconds", default=0.02)
    @option("-s", "--skip-db", action='store_true', help="skip creation of an sqlite db for clip metadata")
    def do_split(self, args):
        "split .wav files on silence thresholds"

        # print(vars(options))
        config = vars(args).copy()
        del config['target']

        if not args.output:
            target = Path(args.target)
            path = target.parent / f'{target.stem}-clips'
        else:
            path = args.output

        col = SampleCollection(path, from_dir=args.target, **config)
        col.split(no_prefix=args.no_prefix)

    @arg("path", help="path to collection folder")
    @option("-s", "--shuffle", action="store_true", help="shuffle result")
    @option("-o", "--output", help="output path to export to", default="wavdb-exported")
    def do_export(self, args):
        "export content from collection"
        result=[]
        for root, dirs, files in os.walk(args.path):
            if root.endswith('_meta'):
                continue
            if not dirs:
                for f in files:
                    p = os.path.join(root, f)
                    result.append(p)
        if args.shuffle:
            random.shuffle(result)
        try:
            os.mkdir(args.output)
        except FileExistsError:
            print("output directory already exists")
            return
        for i, p in enumerate(result):
            i += 1
            name = f"{i:03d}.wav"
            dst = os.path.join(args.output, name)
            shutil.copy(p, dst)
        print("done")




    @arg("path", help="path to source collection")
    @arg("dst", help="path to destination collection")
    @arg("sql", help="sql query to specify clone composition")
    def do_clone(self, args):
        "clone sample collection"
        # print(vars(args))
        col = SampleCollection(args.path)
        col.clone(to=args.dst, sql=args.sql)

    @arg("path", help="path to source collection")
    @arg("sql", help="sql query to specify criteria for deletion")
    @option("-n", "--noconfirm", help="skip confirmation step")
    def do_delete(self, args):
        "delete clips in-place"
        config = self.get_config(args)
        col = SampleCollection(args.path)
        col.delete(args.sql, **config)


    @arg("path", help="path to source collection")
    @arg("dst", help="destination path of shuffled clips")
    @arg("sql", help="sql query to specify clips to be shuffled")
    def do_shuffle(self, args):
        "random shuffle of clips"
        col = SampleCollection(args.path)
        col.shuffle(to=args.dst, sql=args.sql)


    @arg("path", help="path to source collection")
    @arg("dst", help="destination path of modified clips")
    @arg("sql", help="sql query to specify criteria for fx application")
    @arg("chain", nargs="*", help="chain of sox effects")
    @option("-i", "--inplace", action="store_true", help="apply efects in-place")
    def do_fx(self, args):
        "apply an fx chain"
        col = SampleCollection(args.path)
        col.apply_fx(to=args.dst, sql=args.sql, chain=args.chain)

    @arg("target", help=".wav file or folder of .wav files to split")
    @option("-fx", "--apply-fx", help="apply efects in-place")
    @option("-sql", help="sql query")
    def do_test(self, args):
        "testing args"
        print(vars(args))

    def cmdline(self):
        parser = argparse.ArgumentParser(
            # prog = self.name,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description=self.__doc__,
            epilog = self.epilog,
        )

        parser.add_argument('-v', '--version', action='version',
                            version = '%(prog)s '+ self.version)

        ## default arg
        # parser.add_argument('db', help='wav db path')
        parser.add_argument('--db', help='wav db path')

        # non-subcommands here

        subparsers = parser.add_subparsers(
            title='subcommands',
            description='valid subcommands',
            help='additional help',
        )

        for name in sorted(self._argparse_subcmds.keys()):
            subcmd = self._argparse_subcmds[name]
            subparser = subparsers.add_parser(subcmd['name'],
                                     help=subcmd['func'].__doc__)
            for args, kwds in subcmd['options']:
                subparser.add_argument(*args, **kwds)
            subparser.set_defaults(func=subcmd['func'])

        if len(sys.argv) <= 1:
            options = parser.parse_args(self.default_args)
        else:
            options = parser.parse_args()
        options.func(self, options)


if __name__ == '__main__':
    app = Application()
    app.cmdline()

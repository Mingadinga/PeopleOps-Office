"""python3 -m scripts.mission1_dataset {generate,validate,report}"""
import argparse
import json
import hashlib
from pathlib import Path
from .common import DEFAULT_RULES, DEFAULT_OUTPUT, DEFAULT_MANIFEST, ROOT, load_rules, write_data, read_data, file_hashes, dump, compact
from .generate import generate
from .schema import OPTIONAL_TABLES, SCHEMA
from .validate import validate, validate_manifest
from .report import summarize, markdown


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['generate','validate','report'])
    parser.add_argument('--rules',type=Path,default=DEFAULT_RULES)
    parser.add_argument('--output',type=Path,default=DEFAULT_OUTPUT)
    parser.add_argument('--manifest',type=Path,default=DEFAULT_MANIFEST)
    args=parser.parse_args();rules=load_rules(args.rules)
    if rules['dataset_version'] in ('v0.1','v0.2','v0.3') or args.manifest.resolve().parent==(ROOT/'data/generation').resolve() or any(v in args.output.parts for v in ('v0.1','v0.2','v0.3')) or any(part in args.manifest.parts for part in ('synthetic','presentation','v0.1','v0.2','v0.3')):
        parser.exit(1,'Legacy/frozen/presentation artifacts are protected; use v0.4 versioned paths.\n')
    if args.command=='generate':write_data(args.output,generate(rules))
    try:data=read_data(args.output)
    except (OSError,ValueError) as exc:
        parser.exit(1,f'Dataset read error: {exc}\n')
    validation=validate(data,rules)
    if args.command!='generate':
        try:
            manifest=json.loads(args.manifest.read_text(encoding='utf-8'))
            validation['errors'].extend(validate_manifest(manifest,data,rules,args.output,args.rules))
        except (OSError,ValueError,TypeError) as exc:
            validation['errors'].append({'code':'manifest','message':str(exc)})
        if validation['errors']:validation['status']='ERROR'
    artifact_dir=args.manifest.parent
    dump(artifact_dir/'validation_report.json',validation)
    if args.command=='generate':
        hashes=file_hashes(args.output)
        versions={k:rules[k] for k in ('dataset_version','generation_version','generation_rules_version','schema_version','seed','generated_at','observation_start','observation_end','timezone','case_id','job_id')}
        manifest={**versions,'record_counts':{n+'.csv':len(data[n]) for n in SCHEMA if n not in OPTIONAL_TABLES or data.get(n)},
                  'dataset_path':str(args.output.resolve().relative_to(ROOT)) if args.output.resolve().is_relative_to(ROOT) else str(args.output.resolve()),
                  'generation_rules_sha256':hashlib.sha256(args.rules.read_bytes()).hexdigest(),
                  'generator_source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(__file__).parent.glob('*.py'))},
                  'file_sha256':hashes,'validation_status':validation['status'],'validation_errors':validation['errors'],
                  'validation_warnings':validation['warnings'],'review_status':'UNREVIEWED','frozen':False,
                  'timestamp_note':rules['clock_note'],'implementation_parameters':rules['implementation_parameters'],
                  'random_stream_version':rules['random_stream_version'],'capacity_parameters':rules['capacity'],
                  'source_matrix':rules['source_matrix'],'response_window_days':rules['offers']['response_window_days']}
        manifest['record_counts'].update({n+'.json':len(data[n]) if isinstance(data[n],list) else 1 for n in ('workforce_plan','funnel_plan','talent_profile')})
        dump(args.manifest,manifest)
    if validation['errors']:
        dump(artifact_dir/'sanity_report.json',{'scope':'Validation failed; no statistics asserted.','validation':validation})
        (artifact_dir/'sanity_report.md').write_text('# Dataset sanity check failed\n\nValidation ERROR; inspect validation_report.json. Previous statistics are not retained.\n',encoding='utf-8')
        print(compact({'status':'ERROR','errors':validation['errors'][:15],'error_count':len(validation['errors'])}))
        return 1
    report=summarize(data,rules,validation)
    dump(artifact_dir/'sanity_report.json',report)
    (artifact_dir/'sanity_report.md').write_text(markdown(report),encoding='utf-8')
    print(compact({'status':validation['status'],'warnings':validation['warnings'],'funnel':report['funnel'],'workforce':report['workforce']}))
    return 0


if __name__=='__main__':
    raise SystemExit(main())

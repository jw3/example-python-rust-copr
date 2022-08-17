/*
 * Copyright Concurrent Technologies Corporation 2021
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

use crate::error::Error;
use ariadne::{Report, ReportKind, Source};
use fapolicy_rules::parser::errat::{ErrorAt, StrErrorAt};
use fapolicy_rules::parser::parse::StrTrace;
use fapolicy_rules::parser::rule;
use fapolicy_rules::parser::trace::Trace;
use fapolicy_rules::Rule;
use nom::IResult;
use std::fs::File;
use std::io;
use std::io::{BufRead, BufReader};
use std::ops::Range;
use std::path::PathBuf;

use crate::rule_check::Line::{Blank, Comment, RuleDef, SetDec};

type RuleParse<'a> = Result<(StrTrace<'a>, Rule), ErrorAt<StrTrace<'a>>>;

enum Line<'a> {
    Blank,
    Comment(String),
    SetDec,
    RuleDef(RuleParse<'a>),
}

pub fn report_for_file(path: PathBuf) -> Result<(), Error> {
    let filename = path.display().to_string();
    let buff = BufReader::new(File::open(path)?);
    let lines: Result<Vec<String>, io::Error> = buff.lines().collect();

    let contents: Vec<String> = lines?.into_iter().collect();

    let offsets = contents
        .iter()
        .fold(vec![], |mut a: Vec<Range<usize>>, curr| {
            let prev = a.last().unwrap_or(&(0..0));
            let start = match prev.end {
                0 => 0,
                v => v + 1,
            };
            let end = start + curr.len();
            a.push(start..end);
            a
        });

    let results: Vec<(usize, IResult<StrTrace, Rule, StrErrorAt>)> = contents
        .iter()
        .map(|s| {
            if s.trim().is_empty() {
                Blank
            } else if s.starts_with('#') {
                Comment(s.clone())
            } else if s.starts_with('%') {
                SetDec
            } else {
                let x = rule::parse(Trace::new(s)).map_err(|e| match e {
                    nom::Err::Error(e) => ErrorAt::from(e),
                    _ => panic!("unexpectd error state"),
                });
                RuleDef(x)
            }
        })
        .enumerate()
        .filter_map(|(i, r)| match r {
            RuleDef(r) => Some((i, r.map_err(|e| nom::Err::Error(e.shift(offsets[i].start))))),
            _ => None,
        })
        .collect();

    for (lineno, result) in results {
        if result.is_err() {
            let r = to_ariadne_labels(&filename, result).into_iter().rfold(
                Report::build(ReportKind::Error, filename.as_str(), offsets[lineno].start),
                |r, l| r.with_label(l),
            );

            r.finish()
                .print((filename.as_str(), Source::from(contents.join("\n"))))
                .unwrap();
        }
    }
    Ok(())
}

fn to_ariadne_labels<'a>(
    id: &'a str,
    result: IResult<StrTrace, Rule, StrErrorAt>,
) -> Option<ariadne::Label<(&'a str, Range<usize>)>> {
    match result {
        Ok(_) => None,
        Err(nom::Err::Error(e)) => {
            // eprintln!("- [!] {:?}", e);
            // eprintln!("e: {:?}", e.1..e.2);
            Some(ariadne::Label::new((id, e.1..e.2)).with_message(format!("{}", e.0)))
        }
        res => {
            eprintln!("unhandled err {:?}", res);
            None
        }
    }
}

import type { Tokenizer } from '@orama/orama';

const tokenPattern = /[A-Za-z0-9_'-]+|[\p{Script=Han}]+/gu;
const hanPattern = /^\p{Script=Han}+$/u;
const asciiSeparatorPattern = /[_'-]+/g;

function pushUnique(tokens: string[], seen: Set<string>, token: string) {
  if (!token || seen.has(token)) return;
  seen.add(token);
  tokens.push(token);
}

function pushHanTokens(tokens: string[], seen: Set<string>, value: string) {
  pushUnique(tokens, seen, value);

  for (let size = 1; size <= 3; size += 1) {
    if (value.length < size) continue;

    for (let index = 0; index <= value.length - size; index += 1) {
      pushUnique(tokens, seen, value.slice(index, index + size));
    }
  }
}

function pushAsciiTokens(tokens: string[], seen: Set<string>, value: string) {
  pushUnique(tokens, seen, value);

  for (const part of value.split(asciiSeparatorPattern)) {
    pushUnique(tokens, seen, part);
  }
}

export function createSearchTokenizer(): Tokenizer {
  return {
    language: 'qlscript',
    normalizationCache: new Map<string, string>(),
    tokenize(raw) {
      const text = raw.normalize('NFKC').toLowerCase();
      const tokens: string[] = [];
      const seen = new Set<string>();

      for (const match of text.matchAll(tokenPattern)) {
        const value = match[0];

        if (hanPattern.test(value)) {
          pushHanTokens(tokens, seen, value);
        } else {
          pushAsciiTokens(tokens, seen, value);
        }
      }

      return tokens;
    },
  };
}

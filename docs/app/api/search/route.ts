import { source } from '@/lib/source';
import { createSearchTokenizer } from '@/lib/search';
import { createFromSource } from 'fumadocs-core/search/server';

export const revalidate = false;

export const { staticGET: GET } = createFromSource(source, {
  tokenizer: createSearchTokenizer(),
});

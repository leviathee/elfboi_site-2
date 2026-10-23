import { decodePreview } from './clipped-preview-decode.mjs';

self.onmessage = async ({ data: file }) => {
  try { self.postMessage(await decodePreview(file)); }
  catch { self.postMessage(null); } // Preview support never gates restoration.
  finally { self.close(); }
};

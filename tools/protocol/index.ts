export type BuilderRequest={text:string;project?:string}
export type BuilderEvent={type:"message"|"agent"|"artifact"|"error";data:unknown}
export function encodeRequest(request:BuilderRequest):string{return JSON.stringify(request)}
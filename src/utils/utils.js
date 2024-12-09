export const getMaxClass = (data)=>{
  const arr = Object.entries(data.class_ratio);
  return arr.filter(d => d[1] == Math.max(...arr.map(d => d[1])))[0][0];
}
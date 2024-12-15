export const getMaxClass = (data)=>{
  const arr = Object.entries(data.class_ratio);
  return arr.filter(d => d[1] == Math.max(...arr.map(d => d[1])))[0][0];
}

export const generateAcronym = (name) => {
  return name
    .replace(/[.,!()]/g, '')
    .split(' ')
    .filter((word, idx) => idx<=2 && !["INC", "Inc", "LLC", "Corp", "Company"].includes(word))
    // .map(word => word[0].toUpperCase())
    .join(' ');
}

export const groupTalentFlow = (data) => {
  const result = [];
  data.forEach(item => {
      const source = item.from;
      const target = item.to;
      const existingEntry = result.find(entry => entry.source === source && entry.target === target);
      if (existingEntry) {
          existingEntry.coo += 1;
      } 
      else result.push({ source, target, coo: 5 });
  });
  return result;
}
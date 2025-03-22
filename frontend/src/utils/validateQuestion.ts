type ValidationResults = {
  isValid: boolean;
  errorMessage?: string;
};

export const keywords = [
  "mind",
  "body",
  "substance",
  "dualism",
  "monism",
  "physical",
  "mental",
  "material",
  "immaterial",
  "consciousness",
  "reality",
  "perception"
];

export const validateQuestion = (question: string): ValidationResults => {
  if (!question.trim()) {
    return { isValid: false, errorMessage: "Please enter a question." };
  }
  const hasKeyword = keywords.some(keyword => question.toLowerCase().includes(keyword));
  if (!hasKeyword) {
    return { isValid: false, errorMessage: "Your question should relate to mind-body dualism or monism. Try including terms like mind, body, consciousness, etc." };
  }
  return { isValid: true };
};
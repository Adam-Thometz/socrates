export const showQuizScore = (score: number) => {
  let feedback = '';
  let feedbackClass = '';
  
  switch (true) {
    case score >= 90:
      feedback = "Excellent! You have a deep understanding of these philosophical positions.";
      feedbackClass = 'excellent';
      break;
    case score >= 70:
      feedback = "Good job! You grasp the main concepts well.";
      feedbackClass = 'good';
      break;
    case score >= 50:
      feedback = "Not bad. You understand some key differences in these philosophical views.";
      feedbackClass = 'average';
      break;
    default:
      feedback = "Keep studying! These philosophical concepts can be challenging.";
      feedbackClass = 'needs-work';
  }

  return { feedback, feedbackClass };
}
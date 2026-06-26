import api from './api.js';

export const interviewService = {
  async parseJD(jdText, title, company) {
    const payload = { jd_text: jdText };
    if (title) payload.title = title;
    if (company) payload.company = company;
    const response = await api.post('/interviews/parse-jd', payload);
    return response.data;
  },

  async startInterview(jobId) {
    const response = await api.post('/interviews/start', {
      job_id: jobId,
    });
    return response.data;
  },

  async getInterview(interviewId) {
    const response = await api.get('/interviews/' + interviewId);
    return response.data;
  },

  async listInterviews() {
    const response = await api.get('/interviews');
    return response.data;
  },
};

export default interviewService;

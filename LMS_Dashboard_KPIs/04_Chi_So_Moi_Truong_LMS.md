# 4️⃣ CHỈ SỐ ĐÁNH GIÁ MÔI TRƯỜNG LMS & HỌC TẬP SỐ

[← Quay lại README](./README.md)

---

## TỔNG QUAN

Nhóm chỉ số này đánh giá hạ tầng công nghệ, mức độ sẵn sàng số, và trải nghiệm người dùng của hệ thống LMS, bao gồm:
- Hạ tầng và Khả năng Truy cập (Infrastructure & Accessibility)
- Mức độ Sẵn sàng Số (Digital Readiness)
- Trải nghiệm Người dùng (User Experience)
- Hiệu suất Hệ thống (System Performance)

**Tổng số**: 10 chỉ số (7 định lượng + 3 định tính)

---

## A. HẠ TẦNG VÀ KHẢ NĂNG TRUY CẬP

### KPI 4.1: Tỷ lệ Thời gian Hoạt động (System Uptime Rate)

**Mô tả nghiệp vụ**: Phần trăm thời gian LMS hoạt động bình thường, đảm bảo người dùng có thể truy cập mọi lúc.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Uptime Rate = (Total time - Downtime) / Total time × 100%
  
  Tính theo tháng: (720 giờ - downtime hours) / 720 × 100%
  ```
- **Dữ liệu LMS**: 
  - `system_health_log`: downtime incidents, duration
  - Server monitoring tool: Uptime Robot, Pingdom, New Relic
  - Scheduled maintenance vs unplanned outage
- **Mục đích trên dashboard**:
  - Monitor infrastructure reliability
  - SLA compliance (Service Level Agreement)
  - Plan maintenance windows
- **Ngưỡng đánh giá**:
  - Excellent: ≥ 99.5% (3.6 giờ downtime/tháng)
  - Good: 99.0-99.4% (~7 giờ/tháng)
  - Unacceptable: < 99.0%
- **Nguồn tham khảo**: 
  - EDUCAUSE (2020). *Core Data Service: Cloud Computing & Infrastructure*.
  - Link: https://www.educause.edu/research-and-publications/research/core-data-service

---

### KPI 4.2: Tốc độ Tải Trang (Average Page Load Time)

**Mô tả nghiệp vụ**: Thời gian trung bình để tải các trang LMS, ảnh hưởng trực tiếp đến trải nghiệm và mức độ tham gia.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Average Load Time = Median(page load time) across all users
  
  Tính riêng cho:
  - Dashboard/Homepage
  - Course page
  - Quiz/Assessment
  - Video playback start
  ```
- **Dữ liệu LMS**: 
  - Browser Performance API: `window.performance.timing`
  - Google Analytics: Page Speed metrics
  - Real User Monitoring (RUM): LoadTime distribution
- **Mục đích trên dashboard**:
  - Optimize performance bottlenecks
  - Ensure positive UX
  - Mobile vs Desktop comparison
- **Ngưỡng đánh giá**:
  - Excellent: ≤ 2 seconds
  - Acceptable: 2-4 seconds
  - Needs optimization: > 4 seconds
- **Nguồn tham khảo**: 
  - Google (2018). *The Need for Mobile Speed: How Mobile Latency Impacts Publisher Revenue*.
  - Link: https://www.thinkwithgoogle.com/marketing-strategies/app-and-mobile/mobile-page-speed-new-industry-benchmarks/

---

### KPI 4.3: Tỷ lệ Truy cập từ Thiết bị Di động (Mobile Access Rate)

**Mô tả nghiệp vụ**: Phần trăm người dùng truy cập LMS qua smartphone/tablet, phản ánh xu hướng mobile learning.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Mobile Access Rate = (Sessions từ mobile / Total sessions) × 100%
  
  Mobile: smartphone + tablet
  Desktop: PC + laptop
  ```
- **Dữ liệu LMS**: 
  - `session_log.device_type`: User-Agent parsing
  - Analytics: Device breakdown
  - App usage (nếu có mobile app)
- **Mục đích trên dashboard**:
  - Inform responsive design priorities
  - Mobile app development decision
  - Accessibility planning
- **Ngưỡng đánh giá**:
  - Mobile-first LMS: > 50%
  - Hybrid: 30-50%
  - Desktop-dominant: < 30%
- **Nguồn tham khảo**: 
  - UNESCO (2019). *Mobile Learning Week 2019: Artificial Intelligence for Sustainable Development*.
  - Link: https://en.unesco.org/themes/ict-education/mlw2019

---

### KPI 4.4: Chỉ số Khả năng Tiếp cận (Accessibility Index)

**Mô tả nghiệp vụ**: Đánh giá mức độ LMS tuân thủ các tiêu chuẩn accessibility (WCAG 2.1) để phục vụ người khuyết tật.

- **Loại chỉ số**: Định tính (số hóa qua automated test)
- **Công thức tính**: 
  ```
  Accessibility Score = Compliance với WCAG 2.1 Level AA
  
  Tính dựa trên:
  - Automated test (WAVE, aXe): % pages pass
  - Manual review: Keyboard navigation, Screen reader compatibility
  - Alt text coverage: % images có alt text
  - Caption coverage: % videos có subtitles
  
  Thang điểm: 0-100
  ```
- **Dữ liệu LMS**: 
  - Accessibility audit tools: WAVE API results
  - `course_resources`: alt_text field presence, caption_file uploaded
  - User feedback: Disability services reports
- **Mục đích trên dashboard**:
  - Legal compliance (ADA, Section 508)
  - Inclusive education
  - Improve content accessibility
- **Ngưỡng đánh giá**:
  - Fully accessible: ≥ 90/100
  - Partially accessible: 70-89/100
  - Non-compliant: < 70/100
- **Nguồn tham khảo**: 
  - W3C (2018). *Web Content Accessibility Guidelines (WCAG) 2.1*.
  - Link: https://www.w3.org/TR/WCAG21/
  - Seale, J. (2014). *E-Learning and Disability in Higher Education* (2nd ed.). Routledge.
  - ISBN: 978-0415520584

---

## B. MỨC ĐỘ SẴN SÀNG SỐ

### KPI 4.5: Điểm Năng lực Số của Người dùng (Digital Literacy Score)

**Mô tả nghiệp vụ**: Đánh giá kỹ năng công nghệ cơ bản của GV và SV để sử dụng LMS hiệu quả (theo DigComp hoặc ISTE Standards).

- **Loại chỉ số**: Định tính (số hóa từ survey/test)
- **Công thức tính**: 
  ```
  Digital Literacy = Trung bình điểm từ:
  - Self-assessment survey (DigComp 2.2 framework)
    + Information & data literacy (20%)
    + Communication & collaboration (20%)
    + Digital content creation (20%)
    + Safety (20%)
    + Problem solving (20%)
  
  Hoặc: Performance-based test (thực hành trên LMS)
  
  Thang điểm: 1-5 (Foundation, Intermediate, Advanced, Highly Specialized)
  ```
- **Dữ liệu LMS**: 
  - `digital_literacy_survey`: responses per user
  - Onboarding quiz scores
  - Usage patterns: Feature adoption rate
- **Mục đích trên dashboard**:
  - Identify training needs
  - Tailor support resources
  - Predict LMS adoption success
- **Ngưỡng đánh giá**:
  - Advanced: ≥ 4.0/5.0
  - Intermediate: 3.0-3.9/5.0
  - Foundation: < 3.0/5.0
- **Nguồn tham khảo**: 
  - European Commission (2020). *DigComp 2.2: The Digital Competence Framework for Citizens*.
  - Link: https://joint-research-centre.ec.europa.eu/digcomp_en
  - ISTE (2017). *ISTE Standards for Students*.
  - Link: https://www.iste.org/standards/iste-standards-for-students

---

### KPI 4.6: Tỷ lệ Sử dụng Tính năng Nâng cao (Advanced Features Adoption Rate)

**Mô tả nghiệp vụ**: Phần trăm người dùng khai thác các tính năng nâng cao của LMS (H5P, adaptive quiz, learning path, analytics).

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Adoption Rate = (Số users đã dùng ≥ 3 advanced features / Total users) × 100%
  
  Advanced features: Interactive content, Adaptive learning, Gamification,
                      Analytics dashboard, API integration, Custom plugins
  ```
- **Dữ liệu LMS**: 
  - `feature_usage_log`: user_id, feature_name, usage_count
  - Track: H5P activity creation, Badge earned, Learning path completion
- **Mục đích trên dashboard**:
  - Measure return on investment (advanced LMS)
  - Identify power users vs basic users
  - Training effectiveness
- **Ngưỡng đánh giá**:
  - High adoption: ≥ 40%
  - Moderate: 20-39%
  - Low (underutilization): < 20%
- **Nguồn tham khảo**: 
  - Rogers, E. M. (2003). *Diffusion of Innovations* (5th ed.). Free Press.
  - ISBN: 978-0743222099

---

## C. TRẢI NGHIỆM NGƯỜI DÙNG

### KPI 4.7: Điểm Trải nghiệm Người dùng (User Experience Score - UXS)

**Mô tả nghiệp vụ**: Đánh giá tổng thể về tính dễ sử dụng, thiết kế giao diện, và sự hài lòng khi tương tác với LMS.

- **Loại chỉ số**: Định tính (số hóa từ survey)
- **Công thức tính**: 
  ```
  UX Score = Trung bình từ System Usability Scale (SUS) hoặc tùy chỉnh:
  - Ease of use (25%): "LMS dễ học và sử dụng"
  - Efficiency (25%): "Tôi hoàn thành công việc nhanh chóng"
  - Error handling (20%): "Hệ thống ít lỗi, dễ phục hồi"
  - Satisfaction (30%): "Tôi thích sử dụng LMS này"
  
  Thang điểm: 0-100 (SUS) hoặc 1-5 (Likert)
  ```
- **Dữ liệu LMS**: 
  - `ux_survey`: SUS questionnaire (10 items)
  - Net Promoter Score (NPS)
  - Heatmap/Session recording analysis (Hotjar, FullStory)
- **Mục đích trên dashboard**:
  - Benchmark UX quality
  - Prioritize UI/UX improvements
  - Compare before/after redesign
- **Ngưỡng đánh giá**:
  - Excellent: ≥ 80/100 (SUS)
  - Good: 68-79/100 (SUS average)
  - Poor: < 68/100
- **Nguồn tham khảo**: 
  - Brooke, J. (1996). "SUS: A 'quick and dirty' usability scale". *Usability Evaluation in Industry*, 189-194.
  - Link: https://www.usability.gov/how-to-and-tools/methods/system-usability-scale.html

---

### KPI 4.8: Tỷ lệ Yêu cầu Hỗ trợ Kỹ thuật (Technical Support Request Rate)

**Mô tả nghiệp vụ**: Số lượng tickets/yêu cầu trợ giúp kỹ thuật, phản ánh độ phức tạp và vấn đề của hệ thống.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Support Request Rate = (Số tickets / Tổng số users hoạt động) per tháng
  
  Phân loại:
  - Critical (login issues, data loss): priority 1
  - Major (feature not working): priority 2  
  - Minor (how-to questions): priority 3
  ```
- **Dữ liệu LMS**: 
  - `support_tickets`: ticket_id, category, priority, creation_date, resolution_time
  - Help desk system: Zendesk, Freshdesk integration
- **Mục đích trên dashboard**:
  - Monitor system stability
  - Identify common pain points
  - Help center content gaps
- **Ngưỡng đánh giá**:
  - Low (stable system): < 5% users submit tickets/tháng
  - Moderate: 5-10%
  - High (problematic): > 10%
- **Nguồn tham khảo**: 
  - EDUCAUSE (2021). *IT Support Services: Benchmarking*.
  - Link: https://library.educause.edu/

---

### KPI 4.9: Thời gian Giải quyết Sự cố Trung bình (Mean Time to Resolution - MTTR)

**Mô tả nghiệp vụ**: Thời gian trung bình từ khi báo cáo sự cố đến khi được giải quyết hoàn toàn.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  MTTR = Trung bình(resolution_time - creation_time) per priority
  
  Tính riêng cho:
  - Critical issues: Target ≤ 4 giờ
  - Major: Target ≤ 24 giờ
  - Minor: Target ≤ 72 giờ
  ```
- **Dữ liệu LMS**: 
  - `support_tickets`: creation_timestamp, resolution_timestamp, priority
  - SLA tracking
- **Mục đích trên dashboard**:
  - Measure support team efficiency
  - Ensure SLA compliance
  - User satisfaction
- **Ngưỡng đánh giá**:
  - Excellent: MTTR (critical) ≤ 2 giờ, (major) ≤ 12 giờ
  - Good: MTTR (critical) ≤ 4 giờ, (major) ≤ 24 giờ
  - Needs improvement: Vượt SLA targets
- **Nguồn tham khảo**: 
  - ITIL Foundation (2019). *ITIL 4: Service Management Framework*.
  - Link: https://www.axelos.com/certifications/itil-service-management

---

## D. HIỆU SUẤT HỆ THỐNG

### KPI 4.10: Chỉ số Bảo mật và Quyền riêng tư (Security & Privacy Index)

**Mô tả nghiệp vụ**: Đánh giá mức độ bảo vệ dữ liệu người dùng, tuân thủ GDPR/PDPA, và an ninh hệ thống.

- **Loại chỉ số**: Định tính (checklist-based scoring)
- **Công thức tính**: 
  ```
  Security Index = Compliance score:
  - Data encryption (in transit & at rest) (20%)
  - User authentication & authorization (MFA, SSO) (20%)
  - Privacy policy & consent management (GDPR/PDPA) (20%)
  - Regular security audits & penetration testing (20%)
  - Incident response plan (20%)
  
  Thang điểm: 0-100
  ```
- **Dữ liệu LMS**: 
  - Security audit reports
  - Compliance checklist: GDPR, FERPA, COPPA
  - `security_incidents`: count, severity, response time
  - Vulnerability scan results
- **Mục đích trên dashboard**:
  - Risk management
  - Legal compliance
  - User trust
- **Ngưỡng đánh giá**:
  - Highly secure: ≥ 85/100
  - Moderately secure: 70-84/100
  - Vulnerable: < 70/100
- **Nguồn tham khảo**: 
  - ISO/IEC 27001:2013. *Information Security Management*.
  - Link: https://www.iso.org/isoiec-27001-information-security.html
  - European Commission. *General Data Protection Regulation (GDPR)*.
  - Link: https://gdpr.eu/

---

## TỔNG KẾT NHÓM 4

### Phân loại KPIs theo Stakeholder

**IT Department / System Admin**:
- **KPI 4.1** - Uptime (critical SLA metric)
- **KPI 4.2** - Page load time (performance optimization)
- **KPI 4.8, 4.9** - Support metrics (team efficiency)
- **KPI 4.10** - Security (risk mitigation)

**Academic Leadership / LMS Manager**:
- **KPI 4.3** - Mobile access (strategic planning)
- **KPI 4.4** - Accessibility (compliance & equity)
- **KPI 4.6** - Feature adoption (ROI measurement)
- **KPI 4.7** - User experience (satisfaction)

**Professional Development / Training Team**:
- **KPI 4.5** - Digital literacy (training needs)
- **KPI 4.6** - Feature adoption (training effectiveness)

### Dashboard Implementation

**System Health Dashboard** (realtime, for IT):
```
┌─────────────────────────────────────┐
│ System Status: ✅ Online (99.8%)    │
│ Current Load Time: 1.8s             │
│ Active Users: 2,543                 │
│ Open Tickets: 12 (2 critical)       │
└─────────────────────────────────────┘
```

**User Experience Dashboard** (monthly, for management):
- UX Score trend: 78 → 82 (+4 points YoY)
- Mobile access: 47% (↑ from 35% last year)
- Accessibility: 88/100 (need caption improvements)
- Support request rate: 6.2% (within target)

**Digital Readiness Dashboard** (semester, for training):
- Faculty digital literacy: 3.8/5.0
- Student digital literacy: 4.1/5.0
- Advanced feature adoption:
  * H5P: 28% faculty
  * Learning paths: 15%
  * Analytics: 42%

### Improvement Cycle
```
Measure → Analyze → Act → Re-measure

Example:
1. KPI 4.2: Load time = 5.2s (poor)
2. Analyze: Large image files, unoptimized database queries
3. Act: Image compression, CDN, query optimization
4. Re-measure: Load time = 2.1s (excellent)
```

---

## NGUỒN THAM KHẢO CHÍNH

1. **Nielsen Norman Group (2020)**. *10 Usability Heuristics for User Interface Design*.
   - Link: https://www.nngroup.com/articles/ten-usability-heuristics/

2. **EDUCAUSE (2020)**. *Learning Management System Evolution: Towards Better Learner Outcomes*.
   - Link: https://library.educause.edu/resources/2020/7/learning-management-system-evolution

3. **World Bank (2020)**. *The Role of Technology in Education: Enhancing Learning and Teaching*.
   - Link: https://www.worldbank.org/en/topic/edutech

4. **European Commission (2020)**. *Digital Education Action Plan (2021-2027)*.
   - Link: https://education.ec.europa.eu/focus-topics/digital-education/action-plan

5. **UNESCO (2020)**. *ICT Competency Framework for Teachers (Version 3)*.
   - Link: https://www.unesco.org/en/digital-education/ict-teachers

6. **W3C Web Accessibility Initiative (WAI)**. *Accessibility Principles*.
   - Link: https://www.w3.org/WAI/fundamentals/accessibility-principles/

---

**Tiếp theo**: [📚 Tài liệu Tham khảo Đầy đủ →](./05_Tai_Lieu_Tham_Khao.md)

[← Quay lại README](./README.md)

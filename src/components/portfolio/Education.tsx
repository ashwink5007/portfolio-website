import { GraduationCap, Award, BookOpen } from "lucide-react";

const certifications = [
  {
    title: "Rising Star - Business (Intermediate)",
    issuer: "Celonis Academy",
    subtitle: "Academic Process Mining Fundamentals",
  },
  {
    title: "Schema Design Patterns Certification",
    issuer: "MongoDB",
    subtitle: "",
  },
];

const Education = () => {
  return (
    <section id="education" className="py-20 md:py-28 bg-background">
      <div className="container mx-auto px-6">
        <div className="max-w-4xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-12 md:mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              Education & <span className="text-accent">Certifications</span>
            </h2>
            <div className="w-20 h-1 bg-accent mx-auto rounded-full" />
          </div>

          {/* Education Cards */}
          <div className="grid md:grid-cols-2 gap-6 mb-12">
            {/* B.Tech */}
            <div className="group bg-card rounded-xl p-6 shadow-card hover:shadow-card-hover transition-all duration-300 border border-border hover:border-accent/30">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center flex-shrink-0 group-hover:bg-accent/20 transition-colors">
                  <GraduationCap className="text-accent" size={24} />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-foreground mb-1">
                    B.Tech in Information Technology
                  </h3>
                  <p className="text-accent font-medium text-sm mb-2">
                    2023 - 2027
                  </p>
                  <p className="text-muted-foreground text-sm mb-2">
                    Sri Ramakrishna Engineering College
                  </p>
                  <p className="text-muted-foreground text-sm mb-3">
                    Coimbatore, Tamil Nadu
                  </p>
                  <div className="inline-flex items-center gap-2 px-3 py-1 bg-secondary rounded-full">
                    <span className="text-sm font-medium text-foreground">CGPA: 7.33</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Higher Secondary */}
            <div className="group bg-card rounded-xl p-6 shadow-card hover:shadow-card-hover transition-all duration-300 border border-border hover:border-accent/30">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center flex-shrink-0 group-hover:bg-accent/20 transition-colors">
                  <BookOpen className="text-accent" size={24} />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-foreground mb-1">
                    Higher Secondary (Computer Maths)
                  </h3>
                  <p className="text-accent font-medium text-sm mb-2">
                    2021 - 2023
                  </p>
                  <p className="text-muted-foreground text-sm mb-2">
                    LVMHSS
                  </p>
                  <p className="text-muted-foreground text-sm mb-3">
                    Madurai, Tamil Nadu
                  </p>
                  <div className="inline-flex items-center gap-2 px-3 py-1 bg-secondary rounded-full">
                    <span className="text-sm font-medium text-foreground">Percentage: 88%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Certifications */}
          <div>
            <h3 className="text-xl font-semibold text-foreground mb-6 flex items-center gap-3">
              <Award className="text-accent" size={24} />
              Certifications
            </h3>
            <div className="grid sm:grid-cols-2 gap-4">
              {certifications.map((cert, index) => (
                <div
                  key={index}
                  className="group bg-secondary/50 rounded-lg p-4 hover:bg-secondary transition-colors border border-transparent hover:border-accent/20"
                >
                  <h4 className="font-medium text-foreground mb-1 text-sm">
                    {cert.title}
                  </h4>
                  <p className="text-accent text-sm font-medium">
                    {cert.issuer}
                  </p>
                  {cert.subtitle && (
                    <p className="text-muted-foreground text-xs mt-1">
                      {cert.subtitle}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Education;

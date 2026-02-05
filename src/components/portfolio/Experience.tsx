import { Briefcase, Award, Calendar } from "lucide-react";

const Experience = () => {
  return (
    <section id="experience" className="py-20 md:py-28 bg-secondary/30">
      <div className="container mx-auto px-6">
        <div className="max-w-4xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-12 md:mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              Experience & <span className="text-accent">Achievements</span>
            </h2>
            <div className="w-20 h-1 bg-accent mx-auto rounded-full" />
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Experience */}
            <div className="bg-card rounded-xl p-6 md:p-8 shadow-card border border-border">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-lg bg-accent/10 flex items-center justify-center">
                  <Briefcase className="text-accent" size={20} />
                </div>
                <h3 className="text-xl font-semibold text-foreground">Experience</h3>
              </div>

              <div className="relative pl-6 border-l-2 border-accent/30">
                <div className="absolute left-0 top-0 w-3 h-3 rounded-full bg-accent -translate-x-[7px]" />
                
                <div className="mb-2">
                  <h4 className="text-lg font-semibold text-foreground">
                    Cyber Security Intern
                  </h4>
                  <p className="text-accent font-medium text-sm">Hackup Technology</p>
                </div>

                <div className="flex items-center gap-2 text-muted-foreground text-sm mb-4">
                  <Calendar size={14} />
                  <span>June – July 2025</span>
                </div>

                <ul className="space-y-2 text-muted-foreground text-sm">
                  <li className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                    Gained hands-on exposure to core cybersecurity concepts, including threat analysis, vulnerabilities, and basic security practices
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                    Learned fundamentals of network security, malware awareness, phishing attacks, and cyber threats
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                    Worked with real-world cyber attack case studies to understand prevention and mitigation techniques
                  </li>
                </ul>
              </div>
            </div>

            {/* Achievements */}
            <div className="bg-card rounded-xl p-6 md:p-8 shadow-card border border-border">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-lg bg-accent/10 flex items-center justify-center">
                  <Award className="text-accent" size={20} />
                </div>
                <h3 className="text-xl font-semibold text-foreground">Achievements</h3>
              </div>

              <div className="relative pl-6 border-l-2 border-accent/30">
                <div className="absolute left-0 top-0 w-3 h-3 rounded-full bg-accent -translate-x-[7px]" />
                
                <div className="bg-secondary/50 rounded-lg p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="px-2 py-0.5 text-xs font-medium bg-accent/10 text-accent rounded">
                      🏆 Third Place
                    </span>
                  </div>
                  <h4 className="text-base font-semibold text-foreground mb-2">
                    Cyber Security Poster Presentation
                  </h4>
                  <p className="text-sm text-muted-foreground mb-2">
                    Inter-College Technical Symposium, SREC
                  </p>
                  <p className="text-sm text-muted-foreground">
                    Designed and presented a technical poster on cybersecurity concepts, threat detection, and digital safety practices.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Experience;

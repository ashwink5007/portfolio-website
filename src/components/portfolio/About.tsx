import { Code, Lightbulb, Target } from "lucide-react";

const About = () => {
  return (
    <section id="about" className="py-20 md:py-28 bg-background">
      <div className="container mx-auto px-6">
        <div className="max-w-4xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-12 md:mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              About <span className="text-accent">Me</span>
            </h2>
            <div className="w-20 h-1 bg-accent mx-auto rounded-full" />
          </div>

          {/* Bio */}
          <p className="text-lg md:text-xl text-muted-foreground leading-relaxed text-center mb-16">
            A dedicated and ambitious B.Tech student in Information Technology with a strong interest in full-stack web development and software engineering. Skilled in front-end and back-end development with modern web technologies and AI, focusing on user experience (UI) and performance. Passionate about delivering clean digital solutions that solve real problems.
          </p>

          {/* Value Props */}
          <div className="grid md:grid-cols-3 gap-6 md:gap-8">
            <div className="group p-6 md:p-8 bg-card rounded-xl shadow-card hover:shadow-card-hover transition-all duration-300 border border-border hover:border-accent/30">
              <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center mb-4 group-hover:bg-accent/20 transition-colors">
                <Code className="text-accent" size={24} />
              </div>
              <h3 className="text-lg font-semibold text-foreground mb-2">
                Full-Stack Development
              </h3>
              <p className="text-muted-foreground text-sm leading-relaxed">
                Building complete web applications from frontend to backend with modern technologies like React, Node.js, and MongoDB.
              </p>
            </div>

            <div className="group p-6 md:p-8 bg-card rounded-xl shadow-card hover:shadow-card-hover transition-all duration-300 border border-border hover:border-accent/30">
              <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center mb-4 group-hover:bg-accent/20 transition-colors">
                <Lightbulb className="text-accent" size={24} />
              </div>
              <h3 className="text-lg font-semibold text-foreground mb-2">
                AI & Innovation
              </h3>
              <p className="text-muted-foreground text-sm leading-relaxed">
                Exploring AI-driven solutions like deepfake detection, combining machine learning with practical applications.
              </p>
            </div>

            <div className="group p-6 md:p-8 bg-card rounded-xl shadow-card hover:shadow-card-hover transition-all duration-300 border border-border hover:border-accent/30">
              <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center mb-4 group-hover:bg-accent/20 transition-colors">
                <Target className="text-accent" size={24} />
              </div>
              <h3 className="text-lg font-semibold text-foreground mb-2">
                User-Focused Design
              </h3>
              <p className="text-muted-foreground text-sm leading-relaxed">
                Creating intuitive interfaces with attention to user experience, performance, and accessibility.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;

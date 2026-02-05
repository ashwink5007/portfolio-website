const skillCategories = [
  {
    title: "Programming Languages",
    skills: ["Java", "Python (Basics)"],
  },
  {
    title: "Frontend",
    skills: ["React.js", "Framer Motion", "HTML", "CSS", "Bootstrap"],
  },
  {
    title: "Backend",
    skills: ["Node.js", "Express.js", "REST APIs"],
  },
  {
    title: "Databases",
    skills: ["MongoDB", "MySQL"],
  },
  {
    title: "Tools & IDE",
    skills: ["Git/GitHub", "Docker", "Postman", "VS Code"],
  },
  {
    title: "Design & Media",
    skills: ["Canva", "Adobe Express", "Figma (basic)", "CapCut", "Adobe Premiere Pro", "Adobe After Effects"],
  },
];

const Skills = () => {
  return (
    <section id="skills" className="py-20 md:py-28 bg-secondary/30">
      <div className="container mx-auto px-6">
        <div className="max-w-5xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-12 md:mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              Technical <span className="text-accent">Skills</span>
            </h2>
            <div className="w-20 h-1 bg-accent mx-auto rounded-full" />
          </div>

          {/* Skills Grid */}
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {skillCategories.map((category, index) => (
              <div
                key={category.title}
                className="group bg-card rounded-xl p-6 shadow-card hover:shadow-card-hover transition-all duration-300 border border-border hover:border-accent/30"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <h3 className="text-base font-semibold text-foreground mb-4 pb-3 border-b border-border group-hover:border-accent/30 transition-colors">
                  {category.title}
                </h3>
                <div className="flex flex-wrap gap-2">
                  {category.skills.map((skill) => (
                    <span
                      key={skill}
                      className="px-3 py-1.5 text-sm bg-secondary text-secondary-foreground rounded-full hover:bg-accent hover:text-accent-foreground transition-colors cursor-default"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Skills;

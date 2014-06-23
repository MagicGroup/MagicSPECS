Name:           munge-maven-plugin
Version:        1.0
Release:        4%{?dist}
Summary:        Munge Maven Plugin
License:        CDDL
URL:            http://github.com/sonatype/munge-maven-plugin
BuildArch:      noarch

Source0:        https://github.com/sonatype/munge-maven-plugin/archive/munge-maven-plugin-1.0.tar.gz

BuildRequires:  maven-local
BuildRequires:  sonatype-plugins-parent

%description
Munge is a purposely-simple Java preprocessor. It only supports
conditional inclusion of source based on defined strings of the
form "if[tag]", "if_not[tag]", "else[tag]", and "end[tag]".
Unlike traditional preprocessors, comments, and formatting are all
preserved for the included lines. This is on purpose, as the output
of Munge will be distributed as human-readable source code.

To avoid creating a separate Java dialect, the conditional tags are
contained in Java comments. This allows one build to compile the
source files without pre-processing, to facilitate faster incremental
development. Other builds from the same source have their code contained
within that comment. The format of the tags is a little verbose, so
that the tags won't accidentally be used by other comment readers
such as javadoc. Munge tags must be in C-style comments;
C++-style comments may be used to comment code within a comment.

Like any preprocessor, developers must be careful not to abuse its
capabilities so that their code becomes unreadable. Please use it
as little as possible.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.

%prep
%setup -q -n %{name}-%{name}-%{version}

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc LICENSE README

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1.0-4
- 为 Magic 3.0 重建

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-3
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-2
- Fix unowned directory

* Tue Sep 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-1
- Initial packaging

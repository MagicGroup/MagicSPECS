%global gem_name rmail-sup

Summary: A lightweight mail library written in ruby
Name: rubygem-%{gem_name}
Version: 1.0.1
Release: 3%{?dist}
License: BSD
URL: http://sup.rubyforge.org/
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem

Requires: ruby(rubygems)
Requires: rubygem(rmail)

BuildRequires: rubygems-devel

BuildArch: noarch

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}


%description
RMail is a lightweight mail library containing various utility classes and
modules that allow ruby scripts to parse, modify, and generate MIME mail
messages.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install
rm -fr %{_builddir}/%{gem_name}-%{version}%{gem_dir}/gems/%{gem_name}-%{version}/test
chmod a+x %{_builddir}/%{gem_name}-%{version}%{gem_dir}/gems/%{gem_name}-%{version}/lib/rmail/mailbox.rb
chmod a+x %{_builddir}/%{gem_name}-%{version}%{gem_dir}/gems/%{gem_name}-%{version}/lib/rmail.rb

%install
mkdir -p %{buildroot}%{gem_dir}
mv .%{gem_dir}/* %{buildroot}%{gem_dir}


%files
%doc NOTES README THANKS NEWS
%dir %{gem_instdir}
%{gem_instdir}/*
%{gem_cache}
%{gem_spec}

%files doc
%{gem_docdir}


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 1.0.1-2
- Remove unnecessary build requires.
- Corrected License
- Minor changes as per review

* Sat May 09 2015 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 1.0.1-1
- Initial commit

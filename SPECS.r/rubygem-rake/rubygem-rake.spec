# Generated from rake-0.7.3.gem by gem2rpm -*- rpm-spec -*-
%global	majorver	10.0.4
#%%global	preminorver	.beta.5
%global	rpmminorver	.%(echo %preminorver | sed -e 's|^\\.\\.*||')
%global	fullver	%{majorver}%{?preminorver}

%global	gem_name	rake

# Macro overrides which support prelease versions.
%global gem_instdir     %{gem_dir}/gems/%{gem_name}-%{fullver}/
%global gem_docdir      %{gem_dir}/doc/%{gem_name}-%{fullver}/
%global gem_cache       %{gem_dir}/cache/%{gem_name}-%{fullver}.gem
%global gem_spec        %{gem_dir}/specifications/%{gem_name}-%{fullver}.gemspec


%global	fedorarel	1

Summary:	Ruby based make-like utility
Name:		rubygem-%{gem_name}

Version:	%{majorver}
Release:	%{?preminorver:0.}%{fedorarel}%{?preminorver:%{rpmminorver}}%{?dist}.2
Group:		Development/Languages
License:	MIT
URL:		http://rake.rubyforge.org
Source0:	http://rubygems.org/gems/%{gem_name}-%{fullver}.gem

Requires:	ruby(rubygems)
Requires:	ruby(release)
BuildRequires: rubygems-devel
BuildRequires:	ruby(release)
## %%check
#BuildRequires:	ruby(flexmock)
BuildRequires:	rubygem(minitest)
BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
Rake is a Make-like program implemented in Ruby. Tasks and dependencies are
specified in standard Ruby syntax.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
# Directory ownership issue
Requires:	%{name} = %{version}-%{release}

%description    doc
This package contains documentation for %{name}.


%prep
%setup -q -c -T

%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{_prefix}/* %{buildroot}%{_prefix}/

# rpmlint issue
find %{buildroot}%{gem_instdir}/{lib,test} -type f | \
	xargs sed -i -e '\@^#!/usr.*ruby@d'
find %{buildroot}%{gem_instdir}/{doc,lib,test} -type f | xargs chmod 0644

# cleanup
rm %{buildroot}%{gem_instdir}/.gemtest
rm -f %{buildroot}%{gem_instdir}/RRR

# Install man pages into appropriate place.
mkdir -p %{buildroot}%{_mandir}/man1
mv %{buildroot}%{gem_instdir}/doc/rake.1.gz %{buildroot}%{_mandir}/man1

%check
pushd .%{gem_instdir}
ruby -Ilib ./bin/rake test
popd

%files
%defattr(-,root,root,-)
%{_bindir}/rake
%dir	%{gem_instdir}
%doc	%{gem_instdir}/README.rdoc
%doc	%{gem_instdir}/MIT-LICENSE
%doc	%{gem_instdir}/TODO
%doc	%{gem_instdir}/CHANGES
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{_mandir}/man1/*

%files	doc
%defattr(-,root,root,-)
%{gem_instdir}/Rakefile
%{gem_instdir}/install.rb
%{gem_instdir}/doc
%{gem_instdir}/test/
%{gem_docdir}


%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.0.4-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.0.4-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 10.0.4-1
- 10.0.4

* Fri Feb 22 2013 Vít Ondruch <vondruch@redhat.com> - 10.0.3-3
- Rebuid due to error in RubyGems stub shebang.

* Tue Feb 19 2013 Vít Ondruch <vondruch@redhat.com> - 10.0.3-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.0.3-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 10.0.3-1
- 10.0.3

* Tue Jan  1 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 10.0.2-1
- Update to 10.0.2

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2.2-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 09 2012 Vít Ondruch <vondruch@redhat.com> - 0.9.2.2-2
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.2.2-1
- 0.9.2.2

* Sat Jun 11 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.2-1
- 0.9.2

* Sun Jun  5 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.1-2
- Add BR: rubygem(minitest) for %%check

* Sat Jun  4 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.1-1
- 0.9.1

* Thu Mar 18 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.0-0.4.beta.5
- 0.9.0 beta.5

* Mon Mar  7 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.0-0.3.beta.4
- 0.9.0 beta.4

* Fri Mar  4 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.0-0.2.beta.1
- 0.9.0 beta.1

* Thu Feb 24 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.0-0.1.beta.0
- 0.9.0 beta.0
- Split out document files

* Thu Feb 10 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.7-4
- Use BuildRequires, not BuildRequires(check)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.7-1
- 0.8.7
- Enable %%check

* Tue Mar 17 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.8.4-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 27 2008 David Lutterkort <lutter@redhat.com> - 0.8.3-1
- Cleanup multiply listed files
- Set permissions in doc/, lib/ and test/ to 644

* Thu May 15 2008 Alan Pevec <apevec@redhat.com> 0.8.1-2
- fix shebang in scripts

* Thu May 15 2008 Alan Pevec <apevec@redhat.com> 0.8.1-1
- new upstream version

* Thu Aug 23 2007 David Lutterkort <dlutter@redhat.com> - 0.7.3-2
- Fix license tag
- Remove bogus shebangs in lib/ and test/

* Mon Jun 18 2007 David Lutterkort <dlutter@redhat.com> - 0.7.3-1
- Initial package

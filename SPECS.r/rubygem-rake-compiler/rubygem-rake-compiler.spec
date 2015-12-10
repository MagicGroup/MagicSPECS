%global	gemname	rake-compiler
%global	gem_name	%{gemname}
%global	gemdir		%{gem_dir}
%global	geminstdir	%{gem_instdir}

%global	rubyabi	1.8

%if %{?fedora:0%{fedora} >= 17}%{?rhel:0%{rhel} >= 7}
%global	gemdir	%{gem_dir}
%global	gem_name	%{gemname}
%global	geminstdir	%{gem_instdir}
%if 0%{?fedora} < 19
%global	rubyabi	1.9.1
%endif
%global	ruby19	1
%else
%global	ruby19	0
%endif

Summary:	Rake-based Ruby C Extension task generator
Name:		rubygem-%{gemname}
Version:	0.9.5
Release:	5%{?dist}
Group:		Development/Languages
License:	MIT
URL:		http://rake-compiler.rubyforge.org/
Source0:	https://rubygems.org/gems/%{gemname}-%{version}.gem

Requires:	ruby(release)
BuildRequires:	ruby(release)
BuildRequires:	ruby(rubygems) >= 1.3.5
#BuildRequires:	rubygem(cucumber)
#BuildRequires:	rubygem(isolate)
#BuildRequires:	rubygem(rake)
#BuildRequires:	rubygem(rcov)
%if 0%{?fedora} >= 22
BuildRequires:	rubygem(rspec2)
%else
BuildRequires:	rubygem(rspec)
%endif
BuildRequires:	rubygems-devel
Requires:	ruby(rubygems) >= 1.3.5
Requires:	rubygem(rake) >= 0.8.3
BuildArch:	noarch
Provides:	rubygem(%{gemname}) = %{version}-%{release}

%description
rake-compiler aims to help Gem developers while dealing with
Ruby C extensions, simplifiying the code and reducing the duplication.

It follows *convention over configuration* and set an standarized
structure to build and package C extensions in your gems.

This is the result of expriences dealing with several Gems 
that required native extensions across platforms and different 
user configurations where details like portability and 
clarity of code were lacking. 

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}

# rpmlint cosmetic
sed -i -e 's|\r||' README.rdoc
find ./lib/rake -name \*.rb | xargs sed -i -e '\@/usr/bin/env@d'

# Permission
find . -name \*.rb -print0 | xargs --null chmod 0644

gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
%gem_install

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{gemdir}
cp -a .%{_prefix}/* %{buildroot}%{_prefix}/

%check
pushd .%{geminstdir}

# cucumber 0.10.0 needs fixing for newer rake (0.9.0 beta5)
# rake aborted!
# undefined method `desc' for #<Cucumber::Rake::Task:0xb742ebb0>
# rake spec
%if 0%{?fedora} >= 22
cat %{_bindir}/rspec2 | \
	sed -e '\@gem.*rspec-core@i gem "rspec", version' \
	> rspec2
chmod 0755 rspec2
ruby -Ilib -S ./rspec2 spec/
%else
ruby -Ilib -S rspec spec/
%endif

%files
%defattr(-,root,root,-)
%{_bindir}/rake-compiler

%dir %{geminstdir}
%doc %{geminstdir}/README.rdoc
%doc %{geminstdir}/LICENSE.txt
%doc %{geminstdir}/History.txt
%{geminstdir}/cucumber.yml
%exclude	%{geminstdir}/appveyor.yml

%{geminstdir}/bin/
%{geminstdir}/features/
%{geminstdir}/lib/
%{geminstdir}/tasks/

%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-,root,root,-)
%{gemdir}/doc/%{gemname}-%{version}
%exclude	%{geminstdir}/Gemfile
%exclude	%{geminstdir}/Rakefile
%{geminstdir}/spec/


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.9.5-5
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.9.5-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.9.5-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jan  4 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.5-1
- 0.9.5

* Sun Dec 28 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.4-1
- 0.9.4

* Wed Aug 13 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.3-1
- 0.9.3

* Thu Jun 26 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.2-3
- Adjust test suite for ruby 2.1.x

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 19 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.2-1
- 0.9.2

* Thu Aug  8 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.1-1
- 0.9.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.3-3
- Fix test failure with ruby200

* Fri Feb 22 2013 Vít Ondruch <vondruch@redhat.com> - 0.8.3-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Fri Feb 22 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.3-1
- 0.8.3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 24 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.2-2
- Fix BR

* Thu Jan 24 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.2-1
- 0.8.2

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 16 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.8.1-1
- 0.8.1

* Tue Apr 03 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.0-3
- Fix conditionals for F17 to work for RHEL 7 as well.

* Sun Jan 22 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.8.0-2
- Rebuild against ruby 1.9

* Sun Jan 15 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.8.0-1
- 0.8.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.9-3
- F-17: Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 26 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.7.9-2
- Kill BR: rubygem(rcov) for now

* Sat Jun 11 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.7.9-1
- 0.7.9
- %%check now uses rspec, not spec

* Sat Apr 30 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.7.8-1
- 0.7.8

* Mon Apr  4 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.7.7-1
- 0.7.7

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.7.6-1
- 0.7.6

* Tue Nov 30 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.7.5-2
- 0.7.5
- Move more files to -doc
- Now needs rubygem(isolate) and some other rubygem(foo) for BR

* Wed Aug 11 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.7.1-1
- 0.7.1

* Thu Dec 10 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.7.0-1
- 0.7.0

* Wed Jul 29 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6.0-1
- 0.6.0

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5.0-2
- F-12: Mass rebuild

* Thu Jul  2 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5.0-2
- Restore files under %%{geminstdir}/bin

* Thu Jun 11 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5.0-1
- Initial package

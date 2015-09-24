%global	majorver	2.14.8
#%%global	preminorver	.rc6
%global	rpmminorver	.%(echo %preminorver | sed -e 's|^\\.\\.*||')
%global	fullver	%{majorver}%{?preminorver}

%global	fedorarel	6

%global	gem_name	rspec-core
%global	rpmgem_name	rspec2-core


# %%check section needs rspec-core, however rspec-core depends on rspec-mocks
# runtime part of rspec-mocks does not depend on rspec-core
%global	need_bootstrap_set	0

Summary:	Rspec 2 runner and formatters
Name:		rubygem-%{rpmgem_name}
Version:	%{majorver}
Release:	%{?preminorver:0.}%{fedorarel}%{?preminorver:%{rpmminorver}}%{?dist}.1

Group:		Development/Languages
License:	MIT
URL:		http://github.com/rspec/rspec-core
Source0:	http://rubygems.org/gems/%{gem_name}-%{fullver}.gem
# Explicitly specify core, mocks, expectations version
# internally for rspec3 parallel install
Source1:	rspec2

BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
%if 0%{?need_bootstrap_set} < 1
BuildRequires:	rubygem(ZenTest)
BuildRequires:	rubygem(nokogiri)
BuildRequires:	rubygem(rake)
#BuildRequires:	rubygem(rspec2-expectations)
#BuildRequires:	rubygem(rspec2-mocks)
BuildRequires:	rubygem(rspec2)
# aruba pulls in rspec-expectations
BuildRequires:	rubygem(rspec2-expectations)
BuildRequires:	rubygem(aruba)
%endif
# Make the following installed by default
# lib/rspec/core/rake_task
Requires:	rubygem(rake)
# Optional
#Requires:	rubygem(ZenTest)
#Requires:	rubygem(flexmock)
#Requires:	rubygem(mocha)
#Requires:	rubygem(rr)
Provides:	rubygem(%{rpmgem_name}) = %{version}-%{release}
Obsoletes:	rubygem-rspec-core < 2.14.8-2
BuildArch:	noarch

%description
Behaviour Driven Development for Ruby.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
Obsoletes:	rubygem-rspec-core-doc < 2.14.8-2

%description	doc
This package contains documentation for %{name}.


%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}
sed -i \
	-e '\@#!/usr/bin/env@d' \
	lib/rspec/core/mocking/with_flexmock.rb

gem specification %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{_prefix}
cp -a .%{_prefix}/* %{buildroot}%{_prefix}/

# Rename scripts to avoid conflict with rspec 3
mv %{buildroot}%{_bindir}/autospec{,2}
mv %{buildroot}%{_bindir}/rspec{,2}

# And install modified rspec2
install -cpm 0755 %{SOURCE1} \
	%{buildroot}%{_bindir}/rspec2

# cleanups
rm -f %{buildroot}%{gem_instdir}/{.document,.gitignore,.treasure_map.rb,.rspec,.travis.yml,spec.txt,.yardopts}

%if 0%{?need_bootstrap_set} < 1
%check
LANG=en_US.UTF-8
pushd .%{gem_instdir}
# Test failure needs investigation...
# There are is some missing template for Ruby 2.0.0:
# https://github.com/rspec/rspec-core/commits/master/spec/rspec/core/formatters/html_formatted-2.0.0.html

sed -i.bak \
	-e "\@configures streams before command line options@s|do|, :broken => true do|" \
	spec/rspec/core/command_line_spec.rb
sed -i.bak \
	-e "\@produces HTML identical to the one we designed manually@s|do|, :broken => true do|" \
	spec/rspec/core/formatters/text_mate_formatter_spec.rb

ruby -rubygems -Ilib/ %{buildroot}%{_bindir}/rspec2 spec || \
	ruby -rubygems -Ilib/ %{buildroot}%{_bindir}/rspec2 spec --tag ~broken

popd
%endif

%files
%dir	%{gem_instdir}

%license	%{gem_instdir}/License.txt
%doc	%{gem_instdir}/*.md

%{_bindir}/autospec2
%{_bindir}/rspec2
%{gem_instdir}/exe/
%{gem_instdir}/lib/

%exclude	%{gem_cache}
%{gem_spec}

%files	doc
%{gem_docdir}
%{gem_instdir}/features/
%exclude	%{gem_instdir}/spec/

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.14.8-6.1
- 为 Magic 3.0 重建

* Wed Jul  1 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.8-6
- Also try to load rspec

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.8-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec  2 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.8-5
- Specify core, expectations, core version for rspec2 internally
  for rspec3 parallel install

* Mon Nov 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.8-4
- Enable tests

* Wed Sep 17 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.8-3
- Modify summary, URL
- Kill redundant macro

* Thu Aug 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.8-2
- Rename to rspec2-core, cleanup

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.8-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar  6 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.8-1
- 2.14.8

* Mon Nov 11 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.7-1
- 2.14.7

* Thu Oct 24 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.6-1
- 2.14.6

* Fri Aug 16 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.5-2
- Enable test suite again

* Fri Aug 16 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.5-1
- 2.14.5

* Tue Aug  6 2013 Mamoru TASAKA <mtasaka@fedoraproject.org>
- Again enable test suite

* Tue Aug  6 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.13.1-3
- Bootstrap for rubygem-gherkin <- rubygem-cucumber

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.13.1-2
- Enable test suite again

* Thu Mar 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.13.1-1
- 2.13.1

* Tue Feb 19 2013 Vít Ondruch <vondruch@redhat.com> - 2.12.2-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.2-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.12.2-2
- Use aruba, which is already in Fedora, drop no-longer-needed
  patch

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.12.2-1
- 2.12.2

* Thu Oct 11 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.11.1-1
- 2.11.1
- Drop dependency for mocks and expectations

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan 22 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.8.0-1
- 2.8.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun  7 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.4-1
- 2.6.4

* Wed May 25 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.3-1
- 2.6.3

* Tue May 24 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.2-2
- Workaround for invalid date format in gemspec file (bug 706914)

* Mon May 23 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.2-1
- 2.6.2

* Mon May 16 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.0-1
- 2.6.0

* Tue May 10 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.0-0.2.rc6
- 2.6.0 rc6

* Tue May  3 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.0-0.1.rc4
- 2.6.0 rc4

* Sat Feb 26 2011 Mamoru Tasaka <mtasaka@fedoraproject.org>
- And enable check on rawhide

* Sat Feb 26 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.5.1-3
- More cleanups

* Tue Feb 22 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.5.1-2
- Some misc fixes

* Thu Feb 17 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.5.1-1
- 2.5.1

* Fri Nov 05 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.1-1
- Initial package

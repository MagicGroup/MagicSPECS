# Generated from htmlentities-4.0.0.gem by gem2rpm -*- rpm-spec -*-
%global	gem_name		htmlentities

# Some functions removed on 4.2.4. Please don't upgrade this rpm
# to 4.3.0+ on F-14-

Summary:	A module for encoding and decoding (X)HTML entities
Name:		rubygem-%{gem_name}
Version:	4.3.4
Release:	1%{?dist}
Group:		Development/Languages
License:	MIT
URL:		https://github.com/threedaymonk/htmlentities
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires:	ruby(release)
BuildRequires:	ruby(release)

BuildRequires:	rubygems-devel
BuildRequires:	rubygem(test-unit)
Requires:	ruby(rubygems)
BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
HTMLEntities is a simple library to facilitate encoding and 
decoding of named (&yacute; and so on) or numerical (&#123; or &#x12a;) 
entities in HTML and XHTML documents.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
# Directory ownership issue
Requires:	%{name} = %{version}-%{release}
Requires:	ruby(rubygems)

%description	doc
This package contains documentation for %{name}.

%package	-n ruby-%{gem_name}
Summary:	Non-Gem support for %{gem_name}
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Provides:	ruby(%{gem_name}) = %{version}-%{release}

%description	-n ruby-%{gem_name}
This package provides non-Gem support for %{gem_name}.

%prep
# First install rubygems under %%_builddir to execute some
# tests
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

# Cleanups
rm -f %{buildroot}%{gem_instdir}/setup.rb

%check
pushd ./%{gem_instdir}/

sed -i -e '2i gem "test-unit"' test/test_helper.rb

ruby -Ilib:. -e 'Dir.glob("test/*.rb").each{|f| require f}'

%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*
%{gem_instdir}/lib/

%{gem_cache}
%{gem_spec}

%files	doc
%{gem_instdir}/perf/
%{gem_instdir}/test/
%{gem_docdir}/


%changelog
* Mon Jul  6 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.3.4-1
- 4.3.4

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Dec 27 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.3.3-1
- 4.3.3

* Mon Jun  9 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.3.2-2
- Rebuild

* Fri Jun  6 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.3.2-1
- Update to 4.3.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar  7 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.3.1-7
- Clean up

* Tue Mar 05 2013 Vít Ondruch <vondruch@redhat.com> - 4.3.1-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb  5 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 4.3.1-3
- F-17: rebuild against ruby19

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec  4 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 4.3.1-1
- 4.3.1

* Sun Apr 03 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 4.3.0-1
- 4.3.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  1 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 4.2.4-1
- 4.2.4

* Fri Jan 14 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 4.2.3-1
- 4.2.3

* Sun Nov  6 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 4.2.2-1
- 4.2.2

* Sat Apr 11 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 4.2.1-1
- 4.2.1

* Wed Jan 13 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 4.2.0-2.respin1
- 4.2.0 (tarball seems respun)

* Thu Aug 27 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 4.2.0-1
- 4.2.0

* Fri Aug 21 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 4.1.0-1
- 4.1.0

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 4.0.0-3
- F-12: Mass rebuild

* Fri Mar 6 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Cleanups

* Tue Mar 03 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 4.0.0-1
- Initial package

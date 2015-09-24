%global	gem_name	domain_name
%global	rubyabi	1.9.1

Summary:	Domain Name manipulation library for Ruby
Name:		rubygem-%{gem_name}
Version:	0.5.24
Release:	2%{?dist}

Group:		Development/Languages
# See LICENSE.txt
# data/effective_tld_names.dat is not included in binary rpm
License:	BSD and (MPLv1.1 or GPLv2+ or LGPLv2+)
URL:		https://github.com/knu/ruby-domain_name
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires:	ruby(release)
BuildRequires:	ruby(release)

Requires:	ruby(rubygems) 
Requires:	rubygem(unf)
BuildRequires:	rubygems-devel 
# %%check
BuildRequires:	rubygem(minitest)
BuildRequires:	rubygem(shoulda)
BuildRequires:	rubygem(unf)
BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
This is a Domain Name manipulation library for Ruby.
It can also be used for cookie domain validation based on the Public
Suffix List.


%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
Documentation for %{name}

%prep
%setup -q -c -T

TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}

gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

# Clean up
rm -f %{buildroot}%{gem_instdir}/{.document,.gitignore}

%check
pushd .%{gem_instdir}
sed -i.orig \
	-e '/begin/,/end/d' \
	-e '/bundler/d' \
	test/helper.rb

%if 0%{?fedora} >= 21
sed -i.minitest \
	-e 's|Test::Unit::TestCase|Minitest::Test|' \
	test/*.rb
cat > test/unit.rb << EOF
gem "minitest"
require "minitest/autorun"
EOF
%endif

for f in test/test_*.rb
do
	ruby -Ilib:test:. $f
done
popd


%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/Gemfile*
%exclude	%{gem_instdir}/Rakefile
%exclude	%{gem_instdir}/*.gemspec
%exclude	%{gem_instdir}/.travis.yml

%{gem_libdir}
%exclude	%{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}
%exclude	%{gem_instdir}/test/
%exclude	%{gem_instdir}/tool/
%exclude	%{gem_instdir}/data/

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 17 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.24-1
- 0.5.24

* Sun Dec 21 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.23-1
- 0.5.23

* Tue Nov  4 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.22-1
- 0.5.22

* Wed Sep 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.21-1
- 0.5.21

* Sun Aug 31 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.20-1
- 0.5.20

* Fri Jun 27 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.19-1
- 0.5.19

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 08 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.18-2
- Support Minitest 5+

* Mon Apr 07 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.18-1
- 0.5.18

* Sat Feb 15 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.16-1
- 0.5.16

* Tue Nov 19 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.15-1
- 0.5.15

* Tue Oct 22 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.14-1
- 0.5.14

* Fri Oct 11 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.13-2
- Remove redundant BR

* Tue Oct  8 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.13-1
- 0.5.13

* Mon Apr 29 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.11-1
- 0.5.11

* Fri Mar 22 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.9-1
- 0.5.9

* Sun Jan 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.7-2
- A bit clean up

* Sun Jan 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.7-1
- Initial package

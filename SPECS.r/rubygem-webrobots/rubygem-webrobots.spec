%global	gem_name	webrobots
%if 0%{?fedora} < 19
%global	rubyabi	1.9.1
%endif

Summary:	Ruby library to help write robots.txt compliant web robots
Name:		rubygem-%{gem_name}
Version:	0.1.1
Release:	4%{?dist}

Group:		Development/Languages
# LICENSE.txt
License:	BSD
URL:		https://github.com/knu/webrobots
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem

%if 0%{?fedora} >= 19
Requires:	ruby(release)
BuildRequires:	ruby(release)
%else
Requires:	ruby(abi) = %{rubyabi}
Requires:	ruby 
BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby 
%endif

Requires:	ruby(rubygems) 
Requires:	ruby
# Add nokogiri dependency
Requires:	rubygem(nokogiri)
BuildRequires:	rubygems-devel 
BuildRequires:	ruby
# %%check
# F-19: kill check until should is rebuilt
%if 0%{?fedora} < 19
BuildRequires:	rubygem(minitest)
BuildRequires:	rubygem(shoulda)
BuildRequires:	rubygem(nokogiri)
%endif
BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
This library helps write robots.txt compliant web robots in Ruby.


%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
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
mkdir -p .%{gem_dir}


# TODO
# Currently rdoc generation fails with
# f19-ruby: need investigating
gem install \
	-V \
	--local \
	--install-dir .%{gem_dir} \
	--bindir .%{_bindir} \
	--force \
%if 0%{?fedora} < 19
	--rdoc \
%else
	--ri \
%endif
	--backtrace \
	%{gem_name}-%{version}.gem

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

# Clean up
rm -f %{buildroot}%{gem_instdir}/{.document,.gitignore,.travis*}

%check
%if 0%{?fedora} < 19
pushd .%{gem_instdir}
sed -i.orig \
	-e '/begin/,/end/d' \
	-e '/bundler/d' \
	test/helper.rb
# Some tests need net connection
ruby -Ilib:test test/test_webrobots.rb || echo "Investigate this"
popd
%endif

%files
%dir	%{gem_instdir}/
%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/Gemfile*
%exclude	%{gem_instdir}/Rakefile
%exclude	%{gem_instdir}/*.gemspec

%{gem_instdir}/lib/
%exclude	%{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}/
%exclude	%{gem_instdir}/test/

%changelog
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 11 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.1-1
- 0.1.1

* Fri Mar 08 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.0-2
- F-19: rebuild for ruby 2.0.0

* Thu Mar 07 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.0-1
- 0.1.0

* Mon Jan 07 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.0.13-1
- Initial package

%global	gem_name	ruby-ntlm

%if 0%{?fedora} < 19
%global	rubyabi	1.9.1
%endif

%if 0%{?fedora} >= 21
%global	gem_minitest	rubygem(minitest4)
%else
%global	gem_minitest	rubygem(minitest)
%endif

Summary:	NTLM implementation for Ruby
Name:		rubygem-%{gem_name}
Version:	0.0.1
Release:	8%{?dist}

Group: Development/Languages
# README.markdown
License:	MIT
URL:		http://github.com/macks/ruby-ntlm
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch0:	rubygem-ruby-ntlm-0.0.1-test-suite-is-binary.patch

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
BuildRequires:	rubygems-devel 
BuildRequires:	rubygem(test-unit)
BuildRequires:	ruby
# %%check
BuildRequires:	%gem_minitest

BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
NTLM implementation for Ruby.


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

%patch0 -p1

gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
mkdir -p .%{gem_dir}
gem install \
	--local \
	--install-dir .%{gem_dir} \
	-V \
	--force \
	%{gem_name}-%{version}.gem

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
ruby -Ilib:test:. -e 'gem "minitest", "<5" ; Dir.glob("test/*_test.rb").each{|f| require f}'
popd


%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/Rakefile

%{gem_libdir}
%exclude	%{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}
%doc	%{gem_instdir}/examples/
%exclude	%{gem_instdir}/test/
%exclude	%{gem_instdir}/unused/

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.0.1-8
- 为 Magic 3.0 重建

* Tue Jun 23 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.0.1-7
- BR: rubygem(test-unit)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 12 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.0.1-5
- Force to use minitest ver4 for now

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 10 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.0.1-2
- F-19: rebuild for ruby 2.0.0

* Sun Jan 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.0.1-1
- Initial package

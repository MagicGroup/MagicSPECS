%global	gem_name	ensure_valid_encoding
%if 0%{?fedora} >= 21
%global	gem_minitest	rubygem(minitest4)
%else
%global	gem_minitest	rubygem(minitest)
%endif

Name:		rubygem-%{gem_name}
Version:	0.5.3
Release:	5%{?dist}

Summary:	Replace bad bytes in given encoding with replacement strings
License:	MIT
URL:		https://github.com/jrochkind/ensure_valid_encoding
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	%gem_minitest
Requires:	ruby(release)
Requires:	ruby(rubygems)
BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}

%description
Replace bad bytes in given encoding with replacement strings, _or_ 
fail quickly on invalid encodings --  _without_ a transcode to 
a different encoding.

%package	doc
Summary:	Documentation for %{name}
Group:	Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

# Cleanup
pushd %{buildroot}%{gem_instdir}
rm -rf \
	.gitignore \
	Gemfile Rakefile \
	*.gemspec \
	test
popd

%check
pushd .%{gem_instdir}
ruby -Ilib:. -e 'gem "minitest", "<5" ; Dir.glob("test/*_test.rb").each {|f| require f}'
popd

%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*

%{gem_libdir}
%exclude	%{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.5.3-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.5.3-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 12 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.3-2
- Force to use minitest ver4 for now

* Tue Nov 26 2013 TASAKA Mamoru <mtasaka@tbz.t-com.ne.jp> - 0.5.3-1
- Initial package

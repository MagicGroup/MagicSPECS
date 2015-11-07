%global	gem_name	scrub_rb

Name:		rubygem-%{gem_name}
Version:	1.0.1
Release:	5%{?dist}
Summary:	Pure-ruby polyfill of MRI 2.1 String#scrub

License:	MIT
URL:		https://github.com/jrochkind/scrub_rb
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:	rubygems-devel
BuildRequires:	rubygem(minitest) < 5
%if 0%{?fedora} < 21
Requires:	ruby(release)
Requires:	ruby(rubygems)
Provides:	rubygem(%{gem_name}) = %{version}
%endif

BuildArch:	noarch

%description
This gem provides a pure-ruby implementation of 
`String#scrub` and `#scrub!`, monkey-patched into
String, that should work on any ruby platform. 

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

# Cleanups
pushd %{buildroot}%{gem_instdir}
rm -rf \
	.gitignore .travis.yml \
	Gemfile \
	Rakefile \
	*spec \
	benchmark/ \
	test/
popd

%check
pushd .%{gem_instdir}

sed -i -e "2i gem 'minitest', '~> 4'" \
	test/*_test.rb

# As written on borrowed_string_scrub_test.rb
ruby -Ilib:. -e \
	"Dir.glob('test/*_test.rb').each {|f| require f}" \
%if 0%{?fedora} >= 21
	|| \
ruby -Ilib:. -e \
	"Dir.glob('test/*_test.rb').each \
	{|f| require f unless /borrowed_string_scrub_test/ =~ f}"
%else

%endif

popd

%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/README.md
%license	%{gem_instdir}/LICENSE.txt

%{gem_libdir}
%{gem_spec}
%exclude	%{gem_cache}

%files doc
%doc	%{gem_docdir}

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.0.1-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.1-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec  2 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.1-2
- Misc cleanup

* Fri Nov 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.1-1
- Initial package

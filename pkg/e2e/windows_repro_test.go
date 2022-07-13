/*
   Copyright 2020 Docker Compose CLI authors

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

package e2e

import (
	"bytes"
	"strings"
	"sync"
	"testing"
	"time"

	"github.com/compose-spec/compose-go/consts"
	"github.com/stretchr/testify/require"
	"golang.org/x/sync/errgroup"
	"gotest.tools/v3/icmd"
)

func TestWindowsRepro(t *testing.T) {
	const projectName = "win-repro"
	c := NewParallelCLI(
		t, WithEnv(
			consts.ComposeProjectName+"="+projectName,
			consts.ComposeFilePath+"="+"./fixtures/win-repro/compose.yaml",
		),
	)

	resetState := func() {
		c.RunDockerComposeCmdNoCheck(t, "down", "-t", "0")
	}
	resetState()
	defer resetState()

	c.RunDockerComposeCmd(t, "pull")

	stdout := &buffer{}
	cmd := c.NewDockerComposeCmd(t, "up")
	cmd.Timeout = 5 * time.Second
	cmd.Stdout = stdout

	t.Log("=> running compose up")

	var g errgroup.Group
	g.Go(
		func() error {
			res := icmd.RunCmd(cmd)
			t.Logf(
				"EXIT CODE: %d\nERR: %v\nOUTPUT:\n====%s\n====\n",
				res.ExitCode, res.Error, res.Combined(),
			)
			return res.Error
		},
	)

	t.Log("=> waiting for `hello` in logs")
	require.Eventuallyf(
		t, func() bool {
			return strings.Contains(stdout.String(), "hello")
		}, 5*time.Second, 50*time.Millisecond, "container didn't log `hello`:\n====%s\n====", stdout,
	)

	t.Log("=> running compose down")
	c.RunDockerComposeCmd(t, "down", "-t", "0")

	t.Log("=> waiting for compose up to exit")
	require.NoError(t, g.Wait(), "up returned error")
}

type buffer struct {
	mu  sync.RWMutex
	buf bytes.Buffer
}

func (b *buffer) Write(p []byte) (n int, err error) {
	b.mu.Lock()
	defer b.mu.Unlock()
	return b.buf.Write(p)
}

func (b *buffer) String() string {
	b.mu.RLock()
	defer b.mu.RUnlock()
	return b.buf.String()
}
